import nick2bad4u from "eslint-config-nick2bad4u";

/** @type {import("eslint").Linter.Config[]} */
const config = [
    {
        ignores: [".skillcheck-history.json", "tools/**/*.mjs"],
        name: "Generated and local validation tools",
    },
    ...nick2bad4u.createConfig({
        allowDefaultProjectFilePatterns: [],
    }),
    {
        name: "Existing skill release workflow",
        rules: {
            "copilot/require-skill-file-location": "off",
            "repo-compliance/require-release-config-file": "off",
        },
    },
    {
        files: ["stylelint.config.mjs"],
        name: "Stylelint configuration import",
        rules: {
            "@typescript-eslint/no-unsafe-assignment": "off",
        },
    },
];

export default config;
