import 'package:flutter/material.dart';
import '../services/driver_service.dart';

class DriverStatusScreen extends StatefulWidget {
  @override
  _DriverStatusScreenState createState() => _DriverStatusScreenState();
}

class _DriverStatusScreenState extends State<DriverStatusScreen> {
  bool _isOnline = false;
  bool _loading = false;
  String? _error;

  void _toggleStatus(bool value) async {
    setState(() {
      _loading = true;
      _error = null;
    });
    try {
      bool success = await DriverService.setOnlineStatus(value);
      if (success) {
        setState(() {
          _isOnline = value;
        });
      } else {
        setState(() {
          _error = 'Failed to update status';
        });
      }
    } catch (e) {
      setState(() {
        _error = 'Error: $e';
      });
    } finally {
      setState(() {
        _loading = false;
      });
    }
  }

  @override
  void initState() {
    super.initState();
    // TODO: Load initial status from backend
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Statut Chauffeur'),
      ),
      body: Padding(
        padding: EdgeInsets.all(16),
        child: Column(
          children: [
            if (_error != null)
              Text(_error!, style: TextStyle(color: Colors.red)),
            Row(
              mainAxisAlignment: MainAxisAlignment.spaceBetween,
              children: [
                Text('En ligne'),
                _loading
                    ? CircularProgressIndicator()
                    : Switch(
                        value: _isOnline,
                        onChanged: _toggleStatus,
                      ),
              ],
            ),
          ],
        ),
      ),
    );
  }
}
