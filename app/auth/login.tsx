import React, { useState } from "react";
import {
  View,
  Text,
  TextInput,
  TouchableOpacity,
  StyleSheet,
  SafeAreaView,
  StatusBar,
  Alert,
} from "react-native";
import { router } from "expo-router";

import { login } from "../../services/auth";
import { setUser } from "../../services/session";

export default function LoginScreen() {

  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  async function signIn() {

    setUser({
      id: 1,
      name: "EVANS KOENA MOKOATEDI",
      email: "Evanskoena41@gmail.com",
      subscription: "PRO"
    });

    router.replace("/(tabs)");
  }

  return (

    <SafeAreaView style={styles.container}>

      <StatusBar barStyle="light-content" />

      <View style={styles.logoContainer}>

        <Text style={styles.logo}>
          SaintScalperFX
        </Text>

        <Text style={styles.subtitle}>
          AI Trading Command Centre
        </Text>

      </View>

      <View style={styles.form}>

        <Text style={styles.label}>Email</Text>

        <TextInput
          style={styles.input}
          placeholder="Enter your email"
          placeholderTextColor="#7E9DBF"
          autoCapitalize="none"
          keyboardType="email-address"
          value={email}
          onChangeText={setEmail}
        />

        <Text style={styles.label}>Password</Text>

        <TextInput
          style={styles.input}
          placeholder="Enter your password"
          placeholderTextColor="#7E9DBF"
          secureTextEntry
          value={password}
          onChangeText={setPassword}
        />

        <TouchableOpacity
          style={styles.loginButton}
          onPress={signIn}
        >
          <Text style={styles.loginText}>
            LOGIN
          </Text>
        </TouchableOpacity>

        <TouchableOpacity
          onPress={() => router.push("/auth/forgot")}
        >
          <Text style={styles.link}>
            Forgot Password?
          </Text>
        </TouchableOpacity>

        <TouchableOpacity
          onPress={() => router.push("/auth/register")}
        >
          <Text style={styles.link}>
            Create Account
          </Text>
        </TouchableOpacity>

      </View>

    </SafeAreaView>

  );

}

const styles = StyleSheet.create({

  container:{
    flex:1,
    backgroundColor:"#040B18",
    justifyContent:"center",
    paddingHorizontal:25,
  },

  logoContainer:{
    alignItems:"center",
    marginBottom:50,
  },

  logo:{
    fontSize:34,
    fontWeight:"900",
    color:"#00D9FF",
  },

  subtitle:{
    color:"#8FBFFF",
    marginTop:10,
    fontSize:16,
  },

  form:{
    width:"100%",
  },

  label:{
    color:"#CFEAFF",
    marginBottom:8,
    marginTop:15,
    fontWeight:"700",
  },

  input:{
    backgroundColor:"#08172D",
    borderWidth:1,
    borderColor:"#00D9FF",
    borderRadius:14,
    color:"#FFFFFF",
    paddingHorizontal:16,
    paddingVertical:14,
    fontSize:16,
  },

  loginButton:{
    backgroundColor:"#00D9FF",
    marginTop:30,
    borderRadius:14,
    paddingVertical:16,
    alignItems:"center",
  },

  loginText:{
    color:"#00111F",
    fontSize:18,
    fontWeight:"900",
  },

  link:{
    color:"#00D9FF",
    textAlign:"center",
    marginTop:20,
    fontWeight:"700",
  },

});
