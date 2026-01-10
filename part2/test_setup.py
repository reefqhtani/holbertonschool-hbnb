#!/usr/bin/env python3
"""Test the project setup"""

import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    # Test imports
    from app import create_app
    from app.services import facade
    from app.persistence.repository import Repository, InMemoryRepository
    
    print("✓ Project structure is correct")
    print("✓ All imports are working")
    
    # Test facade
    print(f"✓ Facade initialized: {type(facade).__name__}")
    
    # Test repository pattern
    repo = InMemoryRepository()
    print(f"✓ Repository pattern implemented")
    
    # Test Flask app creation
    app = create_app()
    print("✓ Flask app created successfully")
    
    # Check registered endpoints
    print("\n✓ Registered endpoints:")
    for rule in app.url_map.iter_rules():
        if rule.endpoint != 'static':
            print(f"  - {rule.rule}")
    
    print("\n" + "="*50)
    print("✓ All tests passed! Setup is complete.")
    print("="*50)
    print("\nTo run the application:")
    print("  python run.py")
    print("\nAPI Documentation will be at: http://localhost:5000/api/v1/")
    
except Exception as e:
    print(f"✗ Error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
