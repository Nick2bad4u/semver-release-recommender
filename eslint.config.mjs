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
        rules: {
            "copilot/require-skill-file-location": "off",
        },
    },
];

export default config;
