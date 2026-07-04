import { spawnSync } from "node:child_process";
import { mkdirSync } from "node:fs";

const env = {
    ...process.env,
    PYTEST_DISABLE_PLUGIN_AUTOLOAD: "1",
};

mkdirSync(".cache", { recursive: true });

function run(command, args) {
    const result = spawnSync(command, args, {
        env,
        shell: false,
        stdio: "inherit",
    });

    if (result.error) {
        throw result.error;
    }

    if (result.status !== 0) {
        process.exit(result.status ?? 1);
    }
}

run("coverage", [
    "run",
    "-m",
    "pytest",
    "--basetemp=.cache/pytest-tmp",
    "--junitxml=coverage/pytest/junit.xml",
]);
run("coverage", ["xml"]);
run("coverage", ["report"]);
