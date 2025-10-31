"""
Cleanup Python cache files.
Run this when you get import errors after changing files.
"""
import os
import shutil
from pathlib import Path

def remove_pycache(directory):
    """Remove all __pycache__ directories recursively."""
    removed_count = 0
    
    for root, dirs, files in os.walk(directory):
        if '__pycache__' in dirs:
            pycache_path = os.path.join(root, '__pycache__')
            try:
                shutil.rmtree(pycache_path)
                print(f"✓ Removed: {pycache_path}")
                removed_count += 1
            except Exception as e:
                print(f"✗ Failed to remove {pycache_path}: {e}")
    
    return removed_count

def remove_pyc_files(directory):
    """Remove all .pyc files recursively."""
    removed_count = 0
    
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.pyc'):
                file_path = os.path.join(root, file)
                try:
                    os.remove(file_path)
                    print(f"✓ Removed: {file_path}")
                    removed_count += 1
                except Exception as e:
                    print(f"✗ Failed to remove {file_path}: {e}")
    
    return removed_count

if __name__ == "__main__":
    print("=" * 70)
    print("🧹 Cleaning Python Cache Files")
    print("=" * 70)
    
    # Get the backend directory (current directory)
    backend_dir = Path(__file__).parent
    
    print(f"\nScanning directory: {backend_dir}")
    print("-" * 70)
    
    # Remove __pycache__ directories
    print("\n📁 Removing __pycache__ directories...")
    cache_count = remove_pycache(backend_dir)
    
    # Remove .pyc files
    print("\n📄 Removing .pyc files...")
    pyc_count = remove_pyc_files(backend_dir)
    
    print("-" * 70)
    print(f"\n✅ Cleanup complete!")
    print(f"   Removed {cache_count} __pycache__ directories")
    print(f"   Removed {pyc_count} .pyc files")
    print("\n💡 Now restart your backend server")
    print("=" * 70)