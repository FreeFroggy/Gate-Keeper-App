import os
from gatekeeper_vault import initialize_vault_structure, store_script

def test_initialize_vault():
    initialize_vault_structure()
    assert os.path.exists("gatekeeper_vault"), "Vault folder not created"
    print("✅ Vault initialized")

def test_store_script():
    test_file = "test_script.py"
    with open(test_file, "w") as f:
        f.write("print('Hello from test script')")

    result = store_script(test_file)
    assert "stored" in result.lower(), f"Unexpected result: {result}"
    print("✅ Script stored and scanned")

    os.remove(test_file)

def run_all_tests():
    print("🔍 Running Gatekeeper Tests...")
    test_initialize_vault()
    test_store_script()
    print("🎉 All tests passed!")

if __name__ == "__main__":
    run_all_tests()