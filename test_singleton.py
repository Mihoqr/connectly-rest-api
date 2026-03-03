from singletons.config_manager import ConfigManager

print("--- Starting Singleton Test ---")

try:
    config1 = ConfigManager()
    config2 = ConfigManager()

    print(f"Instance 1 ID: {id(config1)}")
    print(f"Instance 2 ID: {id(config2)}")

    # Test 1: Identity Check
    if config1 is config2:
        print("✅ Success: config1 is config2 (Same Instance)")
    else:
        print("❌ Failed: config1 and config2 are different instances")

    # Test 2: Data Sharing Check
    config1.set_setting("DEFAULT_PAGE_SIZE", 50)
    value_from_config2 = config2.get_setting("DEFAULT_PAGE_SIZE")
    
    if value_from_config2 == 50:
        print(f"✅ Success: Shared data is consistent (Value: {value_from_config2})")
    else:
        print("❌ Failed: Data is not shared between instances")

except Exception as e:
    print(f"❌ An error occurred: {e}")

print("--- End of Test ---")