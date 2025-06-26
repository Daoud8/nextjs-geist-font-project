# DjibRide Mobile Apps

This directory contains the Flutter mobile applications for DjibRide platform:

- Passenger App
- Driver App

## Features

- Cross-platform Android and iOS apps
- User registration and login (phone, email, social)
- Payment methods (card, mobile money, cash)
- Real-time GPS tracking and map display
- Ride booking and management
- In-app chat and calls
- Push notifications via Firebase

## Setup

1. Install Flutter SDK: https://flutter.dev/docs/get-started/install
2. Run `flutter pub get` to install dependencies
3. Configure Firebase for push notifications
4. Run the app on emulator or device: `flutter run`

## Project Structure

- `lib/`
  - `main.dart`: App entry point
  - `screens/`: UI screens for passenger and driver
  - `models/`: Data models
  - `services/`: API and business logic
  - `widgets/`: Reusable UI components
  - `utils/`: Utility functions

## Next Steps

- Implement authentication screens and logic
- Implement ride booking and tracking
- Integrate payment gateways
- Implement chat and notifications
