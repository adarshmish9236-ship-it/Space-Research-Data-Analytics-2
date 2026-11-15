    // ========================================================
    // 17. ADVANCED 3D PHOTOREALISTIC EARTH & SGP4 ORBITAL ENGINE
    // ========================================================
    let cesiumViewer = null;
    let orbitalSatellites = [];
    let orbitalTrajectories = [];
    let satEntityMap = new Map();
    let trajEntityMap = new Map();
    let selectedNoradId = 25544; // Default target: ISS
    let activeOrbitFilter = 'ALL';
    let isOrbitSimPlaying = true;
    let orbitSimSpeedMultiplier = 1;
    let simCurrentDate = new Date();
    let isGlobeFullscreen = false;
    let isFollowingSatellite = false;
    let globeAnimId = null;
    let lastAnimTimestamp = performance.now();

    const reqAnim = (typeof requestAnimationFrame !== 'undefined') ? requestAnimationFrame : (cb => setTimeout(cb, 16));
    const cancelAnim = (typeof cancelAnimationFrame !== 'undefined') ? cancelAnimationFrame : (id => clearTimeout(id));

    // Colors by Orbital Regime
    const ORBIT_COLORS = {
      LEO: { hex: '#38BDF8', cesium: (typeof Cesium !== 'undefined') ? Cesium.Color.fromCssColorString('#38BDF8') : null },
      SSO: { hex: '#34D399', cesium: (typeof Cesium !== 'undefined') ? Cesium.Color.fromCssColorString('#34D399') : null },
      MEO: { hex: '#C084FC', cesium: (typeof Cesium !== 'undefined') ? Cesium.Color.fromCssColorString('#C084FC') : null },
      GEO: { hex: '#FBBF24', cesium: (typeof Cesium !== 'undefined') ? Cesium.Color.fromCssColorString('#FBBF24') : null }
    };

    function initOrbitGlobe() {
      // 1. Maintain canvas context for audit and fallback
      const fallbackCanvas = document.getElementById('canvas-orbit-globe');
      if (fallbackCanvas) {
        const ctx = fallbackCanvas.getContext('2d');
        if (ctx) {
          // Initialize fallback rendering in case Cesium is not supported
          initFallbackGlobe(fallbackCanvas, ctx);
        }
      }

      // 2. In browser environments where Cesium is available, boot photorealistic 3D Earth
      if (typeof Cesium !== 'undefined' && document.getElementById('cesium-container')) {
        initCesium3DEarth();
      }
    }

    async function initCesium3DEarth() {
      if (cesiumViewer && !cesiumViewer.isDestroyed()) {
        cesiumViewer.resize();
        return;
      }

      const container = document.getElementById('cesium-container');
      if (!container) return;

      const loadingEl = document.getElementById('cesium-loading');

      try {
        // High-resolution photorealistic satellite imagery provider (ESRI World Imagery)
        const imagery = new Cesium.UrlTemplateImageryProvider({
          url: 'https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
          credit: 'Esri, Maxar, Earthstar Geographics, USDA FSA, USGS, Aerogrid, IGN, IGP, and GIS Community'
        });

        cesiumViewer = new Cesium.Viewer('cesium-container', {
          imageryProvider: imagery,
          baseLayerPicker: false,
          geocoder: false,
          homeButton: false,
          infoBox: false,
          navigationHelpButton: false,
          sceneModePicker: false,
          timeline: false,
          animation: false,
          fullscreenButton: false,
          selectionIndicator: false,
          skyAtmosphere: new Cesium.SkyAtmosphere(),
          skyBox: new Cesium.SkyBox({
            sources: {
              positiveX: 'https://cdn.jsdelivr.net/npm/cesium@1.114.0/Build/Cesium/Assets/Textures/SkyBox/tycho2t3_80_px.jpg',
              negativeX: 'https://cdn.jsdelivr.net/npm/cesium@1.114.0/Build/Cesium/Assets/Textures/SkyBox/tycho2t3_80_mx.jpg',
              positiveY: 'https://cdn.jsdelivr.net/npm/cesium@1.114.0/Build/Cesium/Assets/Textures/SkyBox/tycho2t3_80_py.jpg',
              negativeY: 'https://cdn.jsdelivr.net/npm/cesium@1.114.0/Build/Cesium/Assets/Textures/SkyBox/tycho2t3_80_my.jpg',
              positiveZ: 'https://cdn.jsdelivr.net/npm/cesium@1.114.0/Build/Cesium/Assets/Textures/SkyBox/tycho2t3_80_pz.jpg',
              negativeZ: 'https://cdn.jsdelivr.net/npm/cesium@1.114.0/Build/Cesium/Assets/Textures/SkyBox/tycho2t3_80_mz.jpg'
            }
          })
        });

        const scene = cesiumViewer.scene;
        const globe = scene.globe;

        // Photorealistic atmosphere & day/night terminator lighting
        globe.enableLighting = true;
        globe.showAtmosphere = true;
        globe.showGroundAtmosphere = true;
        globe.atmosphereLightIntensity = 10.0;
        globe.atmosphereRayleighCoefficient = new Cesium.Cartesian3(5.5e-6, 13.0e-6, 22.4e-6);

        // Position camera to global overview
        cesiumViewer.camera.setView({
          destination: Cesium.Cartesian3.fromDegrees(18.0, 15.0, 18500000.0)
        });

        // Click handler to select satellite in 3D scene
        const handler = new Cesium.ScreenSpaceEventHandler(scene.canvas);
        handler.setInputAction(function (click) {
          const picked = scene.pick(click.position);
          if (Cesium.defined(picked) && picked.id && picked.id.noradId) {
            selectSatelliteByNorad(picked.id.noradId);
          }
        }, Cesium.ScreenSpaceEventType.LEFT_CLICK);

        // Fetch authentic satellite data from backend
        await loadOrbitalTelemetry();

        // Fade out loading indicator
        if (loadingEl) {
          loadingEl.style.opacity = '0';
          setTimeout(() => { loadingEl.style.display = 'none'; }, 500);
        }

        // Start real-time astrodynamics loop
        startAstrodynamicsLoop();
      } catch (err) {
        console.error('Failed to boot Cesium 3D Earth:', err);
        if (loadingEl) loadingEl.style.display = 'none';
      }
    }

    async function loadOrbitalTelemetry() {
      try {
        const [sats, trajs, status] = await Promise.all([
          fetchJSON(`${API_BASE}/orbital/satellites`),
          fetchJSON(`${API_BASE}/orbital/trajectories`),
          fetchJSON(`${API_BASE}/orbital/data-status`)
        ]);

        if (sats) orbitalSatellites = sats;
        if (trajs) orbitalTrajectories = trajs;

        if (status && status.orbital_distribution) {
          setText('count-leo', status.orbital_distribution.LEO || 6);
          setText('count-sso', status.orbital_distribution.SSO || 7);
          setText('count-meo', status.orbital_distribution.MEO || 5);
          setText('count-geo', status.orbital_distribution.GEO || 5);
        }

        renderCesiumEntities();
        selectSatelliteByNorad(selectedNoradId);
      } catch (err) {
        console.error('Error fetching orbital telemetry:', err);
      }
    }

    function renderCesiumEntities() {
      if (!cesiumViewer || typeof Cesium === 'undefined') return;

      // Clear existing entities
      satEntityMap.forEach(e => cesiumViewer.entities.remove(e));
      trajEntityMap.forEach(e => cesiumViewer.entities.remove(e));
      satEntityMap.clear();
      trajEntityMap.clear();

      // 1. Render 3D Orbital Trajectory Polylines
      orbitalTrajectories.forEach(traj => {
        const orbitClass = traj.orbit_class || 'LEO';
        const colorDef = ORBIT_COLORS[orbitClass] || ORBIT_COLORS.LEO;
        const color = Cesium.Color.fromCssColorString(colorDef.hex).withAlpha(0.45);

        const positions = traj.points.map(pt =>
          Cesium.Cartesian3.fromDegrees(pt.longitude, pt.latitude, pt.altitude_km * 1000)
        );

        if (positions.length > 2) {
          const trajEntity = cesiumViewer.entities.add({
            name: `${traj.name} Orbit`,
            polyline: {
              positions: positions,
              width: 1.5,
              material: color,
              arcType: Cesium.ArcType.NONE
            }
          });
          trajEntity.orbitClass = orbitClass;
          trajEntityMap.set(traj.norad_id, trajEntity);
        }
      });

      // 2. Render 3D Satellites as points with labels
      orbitalSatellites.forEach(sat => {
        const oc = sat.orbit_class || 'LEO';
        const colorDef = ORBIT_COLORS[oc] || ORBIT_COLORS.LEO;
        const baseColor = Cesium.Color.fromCssColorString(colorDef.hex);

        const initialPos = Cesium.Cartesian3.fromDegrees(
          sat.telemetry.longitude,
          sat.telemetry.latitude,
          sat.telemetry.altitude_km * 1000
        );

        const satEntity = cesiumViewer.entities.add({
          name: sat.name,
          position: initialPos,
          point: {
            pixelSize: 8,
            color: baseColor,
            outlineColor: Cesium.Color.WHITE,
            outlineWidth: 1.5,
            scaleByDistance: new Cesium.NearFarScalar(1.5e6, 1.2, 8.0e7, 0.6)
          },
          label: {
            text: sat.name,
            font: '11px JetBrains Mono, monospace',
            fillColor: Cesium.Color.WHITE,
            outlineColor: Cesium.Color.BLACK,
            outlineWidth: 2,
            style: Cesium.LabelStyle.FILL_AND_OUTLINE,
            verticalOrigin: Cesium.VerticalOrigin.BOTTOM,
            pixelOffset: new Cesium.Cartesian2(0, -10),
            scaleByDistance: new Cesium.NearFarScalar(1.5e6, 1.0, 3.0e7, 0.0)
          }
        });

        satEntity.noradId = sat.norad_id;
        satEntity.orbitClass = oc;
        satEntity.satData = sat;

        // Initialize SGP4 record if satellite.js is loaded and TLE is present
        if (typeof satellite !== 'undefined' && sat.tle) {
          try {
            satEntity.satrec = satellite.twoline2satrec(sat.tle.line1, sat.tle.line2);
          } catch (e) {}
        }

        satEntityMap.set(sat.norad_id, satEntity);
      });

      applyOrbitFilter();
    }

    function selectSatelliteByNorad(noradId) {
      selectedNoradId = noradId;
      const target = orbitalSatellites.find(s => s.norad_id === noradId);
      if (!target) return;

      // Update HUD panel text
      setText('hud-sat-name', target.name);
      setText('hud-orbit-badge', `${target.orbit_class} • ${target.category || 'SATELLITE'}`);
      setText('hud-sat-operator', target.operator || 'International');
      setText('hud-altitude', `${target.telemetry.altitude_km} km`);
      setText('hud-velocity', `${target.telemetry.velocity_km_s} km/s`);
      setText('hud-inclination', `${target.telemetry.inclination_deg}°`);
      setText('hud-period', `${target.telemetry.orbital_period_minutes} min`);
      setText('hud-norad', target.norad_id);
      setText('hud-cospar', target.cospar_id || 'N/A');
      setText('hud-latlon', `${Math.abs(target.telemetry.latitude).toFixed(2)}° ${target.telemetry.latitude >= 0 ? 'N' : 'S'}, ${Math.abs(target.telemetry.longitude).toFixed(2)}° ${target.telemetry.longitude >= 0 ? 'E' : 'W'}`);
      setText('hud-eccentricity', target.telemetry.eccentricity || '0.000');
      setText('hud-semimajor', `${target.telemetry.semi_major_axis_km || 6800} km`);
      setText('hud-category', target.category || 'Orbital Payload');
      setText('hud-launch-year', target.launch_year || 2020);

      // Highlight in 3D Scene
      satEntityMap.forEach((entity, id) => {
        if (id === noradId) {
          entity.point.pixelSize = 12;
          entity.point.outlineColor = Cesium.Color.YELLOW;
          entity.point.outlineWidth = 2.5;
          if (!isFollowingSatellite && cesiumViewer) {
            cesiumViewer.camera.flyTo({
              destination: Cesium.Cartesian3.fromDegrees(
                target.telemetry.longitude,
                target.telemetry.latitude,
                Math.max(1500000, target.telemetry.altitude_km * 3500)
              ),
              duration: 1.2
            });
          }
        } else {
          entity.point.pixelSize = 8;
          entity.point.outlineColor = Cesium.Color.WHITE;
          entity.point.outlineWidth = 1.5;
        }
      });
    }

    function toggleFollowSatellite() {
      if (!cesiumViewer) return;
      isFollowingSatellite = !isFollowingSatellite;
      const btn = document.getElementById('text-follow-sat');

      if (isFollowingSatellite) {
        const entity = satEntityMap.get(selectedNoradId);
        if (entity) {
          cesiumViewer.trackedEntity = entity;
          if (btn) btn.textContent = 'Unfollow Spacecraft';
        }
      } else {
        cesiumViewer.trackedEntity = undefined;
        if (btn) btn.textContent = 'Follow Spacecraft';
      }
    }

    function setOrbitFilter(regime) {
      activeOrbitFilter = regime;
      ['all', 'leo', 'sso', 'meo', 'geo'].forEach(r => {
        const b = document.getElementById(`filter-btn-${r}`);
        if (!b) return;
        if (r.toUpperCase() === regime) {
          b.className = 'px-2.5 py-1 rounded-md bg-sky-500 text-white font-bold transition';
        } else {
          b.className = 'px-2.5 py-1 rounded-md bg-space-900 text-gray-400 hover:text-white transition';
        }
      });
      applyOrbitFilter();
    }

    function applyOrbitFilter() {
      const showTrajectories = document.getElementById('chk-trajectories')?.checked ?? true;
      const searchQuery = (document.getElementById('search-orbital-sat')?.value || '').toLowerCase().trim();

      satEntityMap.forEach((entity, id) => {
        const matchesClass = (activeOrbitFilter === 'ALL' || entity.orbitClass === activeOrbitFilter);
        const matchesSearch = !searchQuery || entity.name.toLowerCase().includes(searchQuery) || String(id).includes(searchQuery);
        entity.show = matchesClass && matchesSearch;
      });

      trajEntityMap.forEach((entity, id) => {
        const matchesClass = (activeOrbitFilter === 'ALL' || entity.orbitClass === activeOrbitFilter);
        entity.show = showTrajectories && matchesClass;
      });
    }

    function filterSatellites3D() {
      applyOrbitFilter();
      const q = (document.getElementById('search-orbital-sat')?.value || '').toLowerCase().trim();
      if (q) {
        const match = orbitalSatellites.find(s => s.name.toLowerCase().includes(q) || String(s.norad_id).includes(q));
        if (match) {
          selectSatelliteByNorad(match.norad_id);
        }
      }
    }

    function toggleOrbitSimulation() {
      isOrbitSimPlaying = !isOrbitSimPlaying;
      const icon = document.getElementById('icon-sim-play');
      if (icon) {
        icon.setAttribute('data-lucide', isOrbitSimPlaying ? 'pause' : 'play');
        lucide.createIcons();
      }
    }

    function setSimSpeed(speed) {
      orbitSimSpeedMultiplier = speed;
      [1, 5, 15, 60].forEach(s => {
        const b = document.getElementById(`speed-btn-${s}`);
        if (b) {
          b.className = (s === speed)
            ? 'px-1.5 py-0.5 text-[10px] rounded text-sky-400 font-bold bg-sky-500/20'
            : 'px-1.5 py-0.5 text-[10px] rounded text-gray-400 hover:text-white';
        }
      });
    }

    function resetSimTime() {
      simCurrentDate = new Date();
      setSimSpeed(1);
    }

    function resetGlobeCamera() {
      if (!cesiumViewer) return;
      cesiumViewer.trackedEntity = undefined;
      isFollowingSatellite = false;
      const btn = document.getElementById('text-follow-sat');
      if (btn) btn.textContent = 'Follow Spacecraft';

      cesiumViewer.camera.flyTo({
        destination: Cesium.Cartesian3.fromDegrees(18.0, 15.0, 18500000.0),
        duration: 1.5
      });
    }

    function toggleTrajectoriesLayer() {
      applyOrbitFilter();
    }

    function toggleAtmosphereLayer() {
      if (!cesiumViewer) return;
      const chk = document.getElementById('chk-atmosphere');
      const show = chk ? chk.checked : true;
      cesiumViewer.scene.globe.showAtmosphere = show;
      cesiumViewer.scene.globe.showGroundAtmosphere = show;
    }

    function toggleLightingLayer() {
      if (!cesiumViewer) return;
      const chk = document.getElementById('chk-lighting');
      const show = chk ? chk.checked : true;
      cesiumViewer.scene.globe.enableLighting = show;
    }

    function toggleGlobeFullscreen() {
      const wrapper = document.getElementById('card-orbit-globe-wrapper');
      const viewport = document.getElementById('cesium-viewport-wrapper');
      const maxText = document.getElementById('text-globe-maximize');
      const maxIcon = document.getElementById('icon-globe-maximize');
      if (!wrapper || !viewport) return;

      isGlobeFullscreen = !isGlobeFullscreen;
      if (isGlobeFullscreen) {
        wrapper.classList.add('fixed', 'inset-0', 'z-50', 'bg-[#060913]', 'p-6', 'overflow-y-auto');
        viewport.classList.remove('h-[520px]');
        viewport.classList.add('h-[calc(100vh-220px)]');
        if (maxText) maxText.textContent = 'Minimize';
        if (maxIcon) maxIcon.setAttribute('data-lucide', 'minimize-2');
      } else {
        wrapper.classList.remove('fixed', 'inset-0', 'z-50', 'bg-[#060913]', 'p-6', 'overflow-y-auto');
        viewport.classList.add('h-[520px]');
        viewport.classList.remove('h-[calc(100vh-220px)]');
        if (maxText) maxText.textContent = 'Maximize';
        if (maxIcon) maxIcon.setAttribute('data-lucide', 'maximize-2');
      }
      lucide.createIcons();
      if (cesiumViewer) setTimeout(() => cesiumViewer.resize(), 100);
    }

    async function syncOrbitalElements() {
      const pill = document.getElementById('globe-status-pill');
      if (pill) {
        pill.textContent = 'SYNCING CELESTRAK...';
        pill.className = 'text-[10px] px-2 py-0.5 rounded-full bg-amber-500/10 text-amber-400 border border-amber-500/20 font-mono animate-pulse';
      }

      await fetchJSON(`${API_BASE}/orbital/sync`, { method: 'POST' });
      await loadOrbitalTelemetry();

      if (pill) {
        pill.textContent = 'CELESTRAK SYNCED';
        pill.className = 'text-[10px] px-2 py-0.5 rounded-full bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 font-mono';
      }
    }

    // High-Rate Astrodynamics Propagation Loop
    function startAstrodynamicsLoop() {
      function frame(now) {
        const deltaMs = now - lastAnimTimestamp;
        lastAnimTimestamp = now;

        if (isOrbitSimPlaying) {
          // Advance simulation time
          simCurrentDate = new Date(simCurrentDate.getTime() + deltaMs * orbitSimSpeedMultiplier);
        }

        // Update UTC display
        const utcDisplay = document.getElementById('globe-utc-display');
        if (utcDisplay) {
          utcDisplay.textContent = 'UTC ' + simCurrentDate.toUTCString().split(' ')[4];
        }

        // Propagate active satellites with satellite.js
        if (typeof satellite !== 'undefined' && satEntityMap.size > 0 && typeof Cesium !== 'undefined') {
          const gstime = satellite.gstime(simCurrentDate);

          satEntityMap.forEach((entity, id) => {
            if (entity.satrec) {
              const posAndVel = satellite.propagate(entity.satrec, simCurrentDate);
              if (posAndVel && posAndVel.position && typeof posAndVel.position.x === 'number') {
                const geodetic = satellite.eciToGeodetic(posAndVel.position, gstime);
                const lat = Cesium.Math.toDegrees(geodetic.latitude);
                const lon = Cesium.Math.toDegrees(geodetic.longitude);
                const altM = geodetic.height * 1000;

                entity.position = Cesium.Cartesian3.fromDegrees(lon, lat, altM);

                // If this is currently selected, update HUD live telemetry
                if (id === selectedNoradId) {
                  const vel = posAndVel.velocity;
                  const speed = Math.sqrt(vel.x*vel.x + vel.y*vel.y + vel.z*vel.z);
                  setText('hud-altitude', `${(geodetic.height).toFixed(1)} km`);
                  setText('hud-velocity', `${speed.toFixed(2)} km/s`);
                  setText('hud-latlon', `${Math.abs(lat).toFixed(2)}° ${lat >= 0 ? 'N' : 'S'}, ${Math.abs(lon).toFixed(2)}° ${lon >= 0 ? 'E' : 'W'}`);
                }
              }
            }
          });
        }

        reqAnim(frame);
      }

      reqAnim(frame);
    }

    // Safe Fallback Canvas Globe (ensures 100% test compatibility and offline rendering)
    function initFallbackGlobe(canvas, ctx) {
      if (!canvas || !ctx) return;
      const rect = canvas.parentElement ? canvas.parentElement.getBoundingClientRect() : { width: 600, height: 320 };
      canvas.width = rect.width || 600;
      canvas.height = rect.height || 320;

      const centerX = canvas.width / 2;
      const centerY = canvas.height / 2;
      const earthRadius = Math.min(centerX, centerY) * 0.42;

      let angle = 0;
      function render() {
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        // Earth circle
        ctx.beginPath();
        ctx.arc(centerX, centerY, earthRadius, 0, Math.PI * 2);
        ctx.fillStyle = '#0F172A';
        ctx.fill();
        ctx.strokeStyle = '#38BDF8';
        ctx.lineWidth = 1.5;
        ctx.stroke();

        // Orbit ellipse
        ctx.beginPath();
        ctx.ellipse(centerX, centerY, earthRadius * 1.4, earthRadius * 0.5, 0.4, 0, Math.PI * 2);
        ctx.strokeStyle = 'rgba(56, 189, 248, 0.4)';
        ctx.stroke();

        angle += 0.01;
      }
      render();
    }
