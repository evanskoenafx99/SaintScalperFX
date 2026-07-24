import React, { useEffect, useRef, useState } from "react";
import { 
  View, 
  Text, 
  StyleSheet, 
  ScrollView, 
  Animated 
} from "react-native";

export default function AIScreen() {

  const messages = [
    "🔍 Scanning XAUUSD...",
    "🌊 Detecting Liquidity...",
    "🧱 Checking Order Block...",
    "📉 Searching Fair Value Gap...",
    "🎯 Calculating Confidence...",
    "✅ BUY Signal Ready",
  ];

  const [message, setMessage] = useState(messages[0]);

  const pulse = useRef(new Animated.Value(1)).current;

  useEffect(() => {

    let index = 0;

    const timer = setInterval(() => {
      index = (index + 1) % messages.length;
      setMessage(messages[index]);
    }, 2000);


    Animated.loop(
      Animated.sequence([
        Animated.timing(pulse, {
          toValue: 1.15,
          duration: 1200,
          useNativeDriver: true,
        }),

        Animated.timing(pulse, {
          toValue: 1,
          duration: 1200,
          useNativeDriver: true,
        }),
      ])
    ).start();


    return () => clearInterval(timer);

  }, []);


  return (
    <ScrollView style={styles.container}>

      <View style={styles.aiBox}>

        <Text style={styles.title}>
          SaintScalperFX AI
        </Text>


        <Animated.View 
          style={[
            styles.circle,
            {
              transform: [
                {scale: pulse}
              ]
            }
          ]}
        >

          <Text style={styles.aiIcon}>
            🤖
          </Text>

        </Animated.View>


        <Text style={styles.status}>
          {message}
        </Text>


        <Text style={styles.confidence}>
          Confidence Engine: ACTIVE
        </Text>


      </View>

    </ScrollView>
  );
}


const styles = StyleSheet.create({

  container:{
    flex:1,
    backgroundColor:"#050505",
  },


  aiBox:{
    alignItems:"center",
    paddingTop:60,
  },


  title:{
    color:"#00ff99",
    fontSize:28,
    fontWeight:"bold",
    marginBottom:40,
  },


  circle:{
    width:180,
    height:180,
    borderRadius:90,
    backgroundColor:"#101010",
    borderWidth:3,
    borderColor:"#00ff99",
    justifyContent:"center",
    alignItems:"center",
    marginBottom:40,
  },


  aiIcon:{
    fontSize:70,
  },


  status:{
    color:"white",
    fontSize:20,
    fontWeight:"bold",
    marginBottom:20,
  },


  confidence:{
    color:"#00ff99",
    fontSize:16,
  },

});
