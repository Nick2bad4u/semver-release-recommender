const sharedConfig = require("secretlint-config-nick2bad4u/secretlintrc.json");

/** @type {import("@secretlint/types").SecretLintConfigDescriptor} */
const secretlintConfig = {
    ...sharedConfig,
    // This skill intentionally documents paths under a user's home directory.
    rules: sharedConfig.rules.filter(
        (rule) => rule.id !== "@secretlint/secretlint-rule-no-homedir"
    ),
};

module.exports = secretlintConfig;
