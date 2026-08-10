import importlib
import importlib.metadata as metadata
import sys

EXPECTED_PYTHON = (3, 13)
EXPECTED_PACKAGES = {
    "numpy": "2.3.5",
    "pandas": "2.3.3",
    "matplotlib": "3.10.1",
    "scikit-learn": "1.7.2",
    "scipy": "1.15.2",
    "xgboost": "3.1.3",
    "joblib": "1.5.2",
    "ipykernel": "6.29.5",
}
MODULE_IMPORTS = (
    "numpy",
    "pandas",
    "matplotlib",
    "sklearn",
    "xgboost",
)


def main() -> int:
    if sys.version_info[:2] != EXPECTED_PYTHON:
        print(
            f"FAIL: Expected Python {EXPECTED_PYTHON[0]}.{EXPECTED_PYTHON[1]} "
            f"but found {sys.version.split()[0]}"
        )
        return 1

    missing = []
    mismatched = []
    for pkg, expected_version in EXPECTED_PACKAGES.items():
        try:
            installed_version = metadata.version(pkg)
        except metadata.PackageNotFoundError:
            missing.append(pkg)
            continue
        if installed_version != expected_version:
            mismatched.append((pkg, expected_version, installed_version))

    if missing:
        print("FAIL: Missing packages:")
        for pkg in missing:
            print(f"  - {pkg}")
        return 1

    if mismatched:
        print("FAIL: Version mismatches:")
        for pkg, expected_version, installed_version in mismatched:
            print(f"  - {pkg}: expected {expected_version}, found {installed_version}")
        return 1

    try:
        for module_name in MODULE_IMPORTS:
            importlib.import_module(module_name)
    except Exception as exc:
        print(f"FAIL: Import check failed: {exc}")
        return 1

    print("OK: Environment is reproducible and ready.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
