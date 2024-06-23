// ignore_for_file: avoid_print
import 'dart:convert';
import 'dart:typed_data';
import 'package:flutter/material.dart';
import 'dart:io';

void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return const MaterialApp(
      home: MyHomePage(),
    );
  }
}

class MyHomePage extends StatefulWidget {
  const MyHomePage({super.key});

  @override
  MyHomePageState createState() {
    return MyHomePageState();
  }
}

class MyHomePageState extends State<MyHomePage> {

  RawDatagramSocket? udpS;
  RawDatagramSocket? udpS2;
  String message = '';
  Uint8List image = Uint8List(1);

  void startListening() async {
    try {
      udpS = await RawDatagramSocket.bind('192.168.0.198',20000);
      udpS2 = await RawDatagramSocket.bind('192.168.0.198',25000);
      udpS!.listen((RawSocketEvent event) {
        if(event == RawSocketEvent.read){
          final datagram = udpS!.receive();
          if(datagram != null){
            final buffer = Uint8List.fromList(datagram.data);
            image = buffer;
            setState(() {});
          }
        }
      });
      udpS2!.listen((event) {
        if(event == RawSocketEvent.read){
          final datagram = udpS2!.receive();
          if(datagram != null){
            final msg = utf8.decode(datagram.data);
            setState(() {
              message = msg;
            });
          }
        }
      });
    } catch (e) {
      print('Error: $e');
    }
  }

  @override
  void initState() {
    super.initState();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text("ESP32 Video Stream"),
      ),
      body: Padding(
          padding: const EdgeInsets.all(16.0),
          child: Column(
            mainAxisAlignment: MainAxisAlignment.start,
            crossAxisAlignment: CrossAxisAlignment.stretch,
            children: [
              const SizedBox(height: 10,),
              Expanded(child: Image.memory(image,gaplessPlayback: true,)),
              const SizedBox(height: 20,),
              const Text('監控訊息：',style: TextStyle(fontWeight: FontWeight.bold)),
              Expanded(
                  child: SingleChildScrollView(
                    child: Text(message,style: const TextStyle(color: Colors.red,fontSize: 25,fontWeight: FontWeight.bold),),
                  )
              ),
              ElevatedButton(
                onPressed: (){
                  startListening();
                },
                child: const Text('連接監控'),
              ),
              const SizedBox(height: 50,),
            ],
          ),
      ),
    );
  }
  @override
  void dispose(){
    udpS?.close();
    super.dispose();
  }
}

