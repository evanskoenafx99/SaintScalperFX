import { Tabs } from "expo-router";
import React from "react";
import { MaterialIcons } from "@expo/vector-icons";

export default function TabLayout() {
  return (
    <Tabs
      screenOptions={{
        headerShown: false,
        tabBarStyle: {
          backgroundColor: "#050816",
          borderTopColor: "#0B1228",
          height: 70,
        },
        tabBarActiveTintColor: "#00AEEF",
        tabBarInactiveTintColor: "#7A869A",
      }}
    >
      <Tabs.Screen
        name="index"
        options={{
          title: "Dashboard",
          tabBarIcon: ({ color, size }) => (
            <MaterialIcons
              name="dashboard"
              size={size}
              color={color}
            />
          ),
        }}
      />

      <Tabs.Screen
        name="markets"
        options={{
          title: "Markets",
          tabBarIcon: ({ color, size }) => (
            <MaterialIcons
              name="show-chart"
              size={size}
              color={color}
            />
          ),
        }}
      />
      <Tabs.Screen
        name="ai"
        options={{
          title: "AI",
          tabBarIcon: ({ color, size }) => (
            <MaterialIcons
              name="smart-toy"
              size={size}
              color={color}
            />
          ),
        }}
      />

      <Tabs.Screen
        name="analytics"
        options={{
          title: "Analytics",
          tabBarIcon: ({ color, size }) => (
            <MaterialIcons
              name="analytics"
              size={size}
              color={color}
            />
          ),
        }}
      />

      <Tabs.Screen
        name="settings"
        options={{
          title: "Settings",
          tabBarIcon: ({ color, size }) => (
            <MaterialIcons
              name="settings"
              size={size}
              color={color}
            />
          ),
        }}
      />
    </Tabs>
  );
}
