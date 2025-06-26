class ChatService {
  // Placeholder chat service for sending and receiving messages

  static Future<bool> sendMessage(String chatId, String message) async {
    // TODO: Implement sending message to backend or Firebase
    print('Sending message to $chatId: $message');
    return true;
  }

  static Stream<String> receiveMessages(String chatId) async* {
    // TODO: Implement receiving messages stream from backend or Firebase
    // For now, yield no messages
  }
}
