import 'package:flutter/material.dart';
import 'screens/home_screen.dart';

void main() {
  runApp(const StudentPerformanceApp());
}

class StudentPerformanceApp extends StatelessWidget {
  const StudentPerformanceApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      debugShowCheckedModeBanner: false,
      title: 'Student Performance Classifier',
      theme: ThemeData(
        primarySwatch: Colors.pink, // or Colors.brown, Colors.deepOrange, etc.
      ),
      home: const HomeScreen(),
    );
  }
}
