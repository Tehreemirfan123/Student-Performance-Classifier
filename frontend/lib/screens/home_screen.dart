import 'package:flutter/material.dart';
import '../services/api_service.dart';

class HomeScreen extends StatefulWidget {
  const HomeScreen({super.key});

  @override
  State<HomeScreen> createState() => _HomeScreenState();
}

class _HomeScreenState extends State<HomeScreen> {
  final _formKey = GlobalKey<FormState>();

  final TextEditingController absencesController = TextEditingController();
  final TextEditingController failuresController = TextEditingController();
  final TextEditingController meduController = TextEditingController();
  final TextEditingController feduController = TextEditingController();
  final TextEditingController g1Controller = TextEditingController();
  final TextEditingController g2Controller = TextEditingController();

  int? selectedStudyTime;
  String predictionResult = '';

  @override
  void dispose() {
    absencesController.dispose();
    failuresController.dispose();
    meduController.dispose();
    feduController.dispose();
    g1Controller.dispose();
    g2Controller.dispose();
    super.dispose();
  }

  void predict() async {
    if (_formKey.currentState!.validate()) {
      try {
        final result = await ApiService.getPrediction(
          studyTime: selectedStudyTime!,
          absences: int.parse(absencesController.text),
          failures: int.parse(failuresController.text),
          medu: int.parse(meduController.text),
          fedu: int.parse(feduController.text),
          g1: int.parse(g1Controller.text),
          g2: int.parse(g2Controller.text),
        );

        // Safely parse predicted grade and probabilities
        final predictedGrade = result['predicted_grade'].toString();

        final probsRaw = result['probabilities'];
        Map<String, dynamic> probs = {};
        if (probsRaw is Map) {
          probs = Map<String, dynamic>.from(probsRaw);
        } else {
          probs = {};
        }

        // Format the probabilities string nicely
        String probText = '';
        probs.forEach((grade, confidence) {
          probText += '$grade: ${(confidence * 100).toStringAsFixed(2)}%\n';
        });

        setState(() {
          predictionResult =
              'Prediction: $predictedGrade\n\nConfidence:\n$probText';
        });
      } catch (e) {
        setState(() {
          predictionResult = 'Error: $e';
        });
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text(
          'Student Performance Classifier',
          style: TextStyle(color: Colors.white),
        ),
        backgroundColor: const Color.fromARGB(255, 96, 8, 8),
        centerTitle: true,
      ),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(16),
        child: Form(
          key: _formKey,
          child: Column(
            children: [
              Center(
                child: Image.asset(
                  'assets/gcu_logo.png',
                  height: 100,
                  width: 100,
                  fit: BoxFit.contain,
                ),
              ),
              const SizedBox(height: 20),
              Theme(
                data: Theme.of(context).copyWith(
                  canvasColor: Colors.white,
                ),
                child: DropdownButtonFormField<int>(
                  value: selectedStudyTime,
                  decoration: const InputDecoration(
                    labelText: 'Study Time (per week)',
                    border: OutlineInputBorder(),
                  ),
                  items: const [
                    DropdownMenuItem(
                        value: 1, child: Text('1 - Less than 2 hours')),
                    DropdownMenuItem(value: 2, child: Text('2 - 5 hours')),
                    DropdownMenuItem(
                        value: 3, child: Text('3 - 5 to 10 hours')),
                    DropdownMenuItem(
                        value: 4, child: Text('4 - More than 10 hours')),
                  ],
                  validator: (value) {
                    if (value == null) {
                      return 'Please select study time';
                    }
                    return null;
                  },
                  onChanged: (value) {
                    setState(() {
                      selectedStudyTime = value;
                    });
                  },
                ),
              ),
              const SizedBox(height: 16),
              TextFormField(
                controller: absencesController,
                keyboardType: TextInputType.number,
                decoration: const InputDecoration(
                  labelText: 'Absences',
                  border: OutlineInputBorder(),
                ),
                validator: (value) {
                  if (value == null || value.isEmpty) {
                    return 'Please enter absences';
                  }
                  return null;
                },
              ),
              const SizedBox(height: 16),
              TextFormField(
                controller: failuresController,
                keyboardType: TextInputType.number,
                decoration: const InputDecoration(
                  labelText: 'Failures',
                  border: OutlineInputBorder(),
                ),
                validator: (value) {
                  if (value == null || value.isEmpty) {
                    return 'Please enter failures';
                  }
                  return null;
                },
              ),
              const SizedBox(height: 16),
              TextFormField(
                controller: meduController,
                keyboardType: TextInputType.number,
                decoration: const InputDecoration(
                  labelText: 'Mother\'s education',
                  border: OutlineInputBorder(),
                ),
                validator: (value) {
                  if (value == null || value.isEmpty) {
                    return 'Please enter mother\'s education';
                  }
                  return null;
                },
              ),
              const SizedBox(height: 16),
              TextFormField(
                controller: feduController,
                keyboardType: TextInputType.number,
                decoration: const InputDecoration(
                  labelText: 'Father\'s education',
                  border: OutlineInputBorder(),
                ),
                validator: (value) {
                  if (value == null || value.isEmpty) {
                    return 'Please enter father\'s education';
                  }
                  return null;
                },
              ),
              const SizedBox(height: 16),
              TextFormField(
                controller: g1Controller,
                keyboardType: TextInputType.number,
                decoration: const InputDecoration(
                  labelText: 'First period grade (G1)',
                  border: OutlineInputBorder(),
                ),
                validator: (value) {
                  if (value == null || value.isEmpty) {
                    return 'Please enter G1 grade';
                  }
                  return null;
                },
              ),
              const SizedBox(height: 16),
              TextFormField(
                controller: g2Controller,
                keyboardType: TextInputType.number,
                decoration: const InputDecoration(
                  labelText: 'Second period grade (G2)',
                  border: OutlineInputBorder(),
                ),
                validator: (value) {
                  if (value == null || value.isEmpty) {
                    return 'Please enter G2 grade';
                  }
                  return null;
                },
              ),
              const SizedBox(height: 24),
              SizedBox(
                width: double.infinity,
                height: 50,
                child: ElevatedButton(
                  style: ElevatedButton.styleFrom(
                    backgroundColor: const Color.fromARGB(255, 96, 8, 8),
                  ),
                  onPressed: predict,
                  child: const Text(
                    'Predict',
                    style: TextStyle(color: Colors.white),
                  ),
                ),
              ),
              const SizedBox(height: 24),
              Text(
                predictionResult,
                style: const TextStyle(fontSize: 18),
                textAlign: TextAlign.center,
              ),
            ],
          ),
        ),
      ),
      bottomNavigationBar: BottomAppBar(
        color: const Color(0xFF600808),
        child: const SizedBox(
          height: 20,
          child: Center(
            child: Text(
              '© GCU University',
              style: TextStyle(color: Colors.white, fontSize: 10),
            ),
          ),
        ),
      ),
    );
  }
}
