import json
import subprocess
import requests
import time

def request_notification_permission():
    try:
        subprocess.run(['termux-notification-remove-all'], check=True)
        print("Permission requested successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error requesting permission: {e}")

def get_notifications():
    try:
        result = subprocess.run(['termux-notification-list'], capture_output=True, text=True)
        notifications = json.loads(result.stdout)
        return notifications
    except Exception as e:
        print(f"Error getting notifications: {e}")
        return []

def forward_notification(notification, webhook_url):
    try:
        payload = {
            'title': notification.get('title'),
            'package': notification.get('packageName'),
            'message': notification.get('content'),
            'timestamp': notification.get('when')
        }
        headers = {'Content-Type': 'application/json'}
        response = requests.post(webhook_url, json=payload, headers=headers)
        if response.status_code == 200:
            print(f"Notification forwarded successfully: {payload}")
        else:
            print(f"Failed to forward notification: {response.status_code}")
    except Exception as e:
        print(f"Error forwarding notification: {e}")

def main():
    webhook_url = input("Masukan URL Webhook: ")
    package_filter = input("Filter Package (Opsional): ")
    package_filter = [pkg.strip() for pkg in package_filter.split(',')] if package_filter else []

    # Request notification permission
    print("Requesting notification access permission...")
    request_notification_permission()
    time.sleep(5)  # Give some time for user to grant permission

    print("Jastif Running...")
    while True:
        notifications = get_notifications()
        for notification in notifications:
            if not package_filter or notification.get('packageName') in package_filter:
                forward_notification(notification, webhook_url)
        time.sleep(10)  # Tunggu 10 detik sebelum mengecek notifikasi lagi

if __name__ == "__main__":
    main()
