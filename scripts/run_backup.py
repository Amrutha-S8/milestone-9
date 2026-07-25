"""
Backup Runner for StayZa Milestone 9.
Creates automated backups and manages retention.
Usage:
    python scripts/run_backup.py [--label daily] [--restore <backup_name>]
"""

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from backup.service import BackupService, RestoreService
from backup.config import BackupConfig


def main():
    parser = argparse.ArgumentParser(description="StayZa Backup & Restore")
    parser.add_argument("--label", default="daily", help="Backup label (default: daily)")
    parser.add_argument("--restore", help="Restore from backup name")
    parser.add_argument("--list", action="store_true", help="List available backups")
    parser.add_argument("--cleanup", action="store_true", help="Cleanup old backups")
    parser.add_argument("--max-backups", type=int, default=30, help="Max backups to keep")
    args = parser.parse_args()

    if args.list:
        svc = BackupService()
        backups = svc.list_backups()
        if not backups:
            print("No backups found.")
            return
        print(f"\nAvailable backups ({len(backups)}):")
        for b in backups:
            print(f"  {b['name']:50s} {b['size_human']:>8s}")
        return

    if args.restore:
        rs = RestoreService()
        rs.restore(args.restore)
        print(f"Restored from: {args.restore}")
        return

    svc = BackupService()
    path = svc.create_backup(label=args.label)
    print(f"Backup created: {path}")

    if args.cleanup:
        svc.cleanup_old_backups(max_backups=args.max_backups)
        print(f"Cleaned up. Max backups retained: {args.max_backups}")


if __name__ == "__main__":
    main()
