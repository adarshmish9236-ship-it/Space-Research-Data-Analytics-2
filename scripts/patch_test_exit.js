const fs = require('fs');

let testScript = fs.readFileSync('scripts/test_ui_subtabs.js', 'utf-8');
testScript = testScript.replace(
  "if (failed > 0) {\n    process.exit(1);\n  }",
  "if (failed > 0) {\n    process.exit(1);\n  } else {\n    process.exit(0);\n  }"
);
fs.writeFileSync('scripts/test_ui_subtabs.js', testScript, 'utf-8');
print = console.log;
print("Added clean process.exit(0) to test_ui_subtabs.js");
