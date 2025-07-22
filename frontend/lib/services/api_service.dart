import 'dart:convert';
import 'package:http/http.dart' as http;

class ApiService {
  static Future<Map<String, dynamic>> getPrediction({
    required int studyTime,
    required int absences,
    required int failures,
    required int medu,
    required int fedu,
    required int g1,
    required int g2,
  }) async {
    final url = Uri.parse('http://192.168.100.31:5000/predict');

    try {
      final response = await http.post(
        url,
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode({
          'studytime': studyTime,
          'absences': absences,
          'failures': failures,
          'Medu': medu,
          'Fedu': fedu,
          'G1': g1,
          'G2': g2,
        }),
      );

      print('Status code: ${response.statusCode}');
      print('Response body: ${response.body}');

      if (response.statusCode == 200) {
        final jsonResponse = jsonDecode(response.body);
        return jsonResponse; // Return Map<String, dynamic>
      } else {
        throw Exception('Failed to get prediction');
      }
    } catch (e) {
      print('HTTP request failed: $e');
      throw Exception('Request error: $e');
    }
  }
}
