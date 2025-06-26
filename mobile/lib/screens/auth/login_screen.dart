import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import '../../services/auth_service.dart';

class LoginScreen extends StatefulWidget {
  final VoidCallback onLoginSuccess;

  LoginScreen({required this.onLoginSuccess});

  @override
  _LoginScreenState createState() => _LoginScreenState();
}

class _LoginScreenState extends State<LoginScreen> {
  final _formKey = GlobalKey<FormState>();
  String _username = '';
  String _password = '';
  bool _loading = false;
  String? _error;

  void _submit() async {
    if (!_formKey.currentState!.validate()) return;
    _formKey.currentState!.save();

    setState(() {
      _loading = true;
      _error = null;
    });

    try {
      bool success = await AuthService.login(_username, _password);
      if (success) {
        widget.onLoginSuccess();
      } else {
        setState(() {
          _error = 'Login failed. Check your credentials.';
        });
      }
    } catch (e) {
      setState(() {
        _error = 'An error occurred: $e';
      });
    } finally {
      setState(() {
        _loading = false;
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Connexion'),
      ),
      body: Padding(
        padding: EdgeInsets.all(16),
        child: Form(
          key: _formKey,
          child: Column(
            children: [
              if (_error != null)
                Text(_error!, style: TextStyle(color: Colors.red)),
              TextFormField(
                decoration: InputDecoration(labelText: 'Email ou téléphone'),
                keyboardType: TextInputType.emailAddress,
                onSaved: (value) => _username = value!.trim(),
                validator: (value) =>
                    value == null || value.isEmpty ? 'Champ requis' : null,
              ),
              TextFormField(
                decoration: InputDecoration(labelText: 'Mot de passe'),
                obscureText: true,
                onSaved: (value) => _password = value!.trim(),
                validator: (value) =>
                    value == null || value.isEmpty ? 'Champ requis' : null,
              ),
              SizedBox(height: 20),
              _loading
                  ? CircularProgressIndicator()
                  : ElevatedButton(
                      onPressed: _submit,
                      child: Text('Se connecter'),
                    ),
            ],
          ),
        ),
      ),
    );
  }
}
