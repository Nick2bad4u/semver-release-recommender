import nick2bad4u from "eslint-config-nick2bad4u";

/** @type {import("eslint").Linter.Config[]} */
const config = [
    {
        ignores: ["tools/**/*.mjs"],
        name: "Local validation tools",
    },
    ...nick2bad4u.configs.all,
    {
        rules: {
            "copilot/require-skill-file-location": "off",
        },
    },
];

export default config;
