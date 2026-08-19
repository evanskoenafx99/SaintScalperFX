import React from "react";

import {
  ScrollView,
  View,
  Text,
  StyleSheet,
  TouchableOpacity,
} from "react-native";

import { useTheme } from "../../context/ThemeContext";

export default function SettingsScreen() {
  const { theme, changeTheme } = useTheme();

  const themeList = [
    {
      name: "Cyber Blue",
      id: "Cyber Blue",
      color: "#00d9ff",
      description: "Clean futuristic AI interface",
    },
    {
      name: "Purple Hologram",
      id: "Purple Hologram",
      color: "#c084fc",
      description: "Holographic intelligence interface",
    },
    {
      name: "Matrix",
      id: "Matrix",
      color: "#00ff88",
      description: "High-contrast intelligence terminal",
    },
    {
      name: "Combat Mode",
      id: "Combat Mode",
      color: "#ff3b30",
      description: "Tactical signal interface",
    },
  ];

  return (
    <ScrollView
      style={[
        styles.container,
        {
          backgroundColor: theme.background,
        },
      ]}
      contentContainerStyle={styles.content}
      showsVerticalScrollIndicator={false}
    >
      {/* HEADER */}

      <Text
        style={[
          styles.title,
          {
            color: theme.primary,
          },
        ]}
      >
        SAINT ULTRA
      </Text>

      <Text style={styles.subtitle}>
        SIGNAL INTELLIGENCE CONTROL CENTER
      </Text>

      {/* APPEARANCE */}

      <Text
        style={[
          styles.section,
          {
            color: theme.text,
          },
        ]}
      >
        APPEARANCE
      </Text>

      <View
        style={[
          styles.panel,
          {
            borderColor: theme.primary,
            backgroundColor: theme.panel,
          },
        ]}
      >
        <Text
          style={[
            styles.panelTitle,
            {
              color: theme.primary,
            },
          ]}
        >
          INTERFACE THEME
        </Text>

        <Text style={styles.panelDescription}>
          Choose the visual identity used throughout SAINT ULTRA.
        </Text>

        {themeList.map((item) => {
          const active = theme.name === item.name;

          return (
            <TouchableOpacity
              key={item.id}
              activeOpacity={0.8}
              onPress={() => changeTheme(item.id)}
              style={[
                styles.themeCard,
                {
                  borderColor: active
                    ? item.color
                    : "rgba(127,162,201,0.25)",
                  backgroundColor: active
                    ? `${item.color}12`
                    : "rgba(255,255,255,0.02)",
                },
              ]}
            >
              <View
                style={[
                  styles.themeIndicator,
                  {
                    backgroundColor: item.color,
                  },
                ]}
              />

              <View style={styles.themeInfo}>
                <Text style={styles.themeName}>
                  {item.name}
                </Text>

                <Text style={styles.themeDescription}>
                  {item.description}
                </Text>
              </View>

              <Text
                style={[
                  styles.themeStatus,
                  {
                    color: active
                      ? item.color
                      : "#60748F",
                  },
                ]}
              >
                {active ? "ACTIVE" : "SELECT"}
              </Text>
            </TouchableOpacity>
          );
        })}
      </View>

      {/* SIGNAL SETTINGS */}

      <Text
        style={[
          styles.section,
          {
            color: theme.text,
          },
        ]}
      >
        SIGNAL INTELLIGENCE
      </Text>

      <View
        style={[
          styles.panel,
          {
            borderColor: theme.primary,
            backgroundColor: theme.panel,
          },
        ]}
      >
        <SettingRow
          title="AI SIGNAL ENGINE"
          value="ONLINE"
          valueColor="#00FF88"
        />

        <SettingRow
          title="LIVE MARKET DATA"
          value="STREAMING"
          valueColor="#00FF88"
        />

        <SettingRow
          title="SIGNAL MODE"
          value="AI ANALYSIS"
          valueColor={theme.primary}
        />

        <SettingRow
          title="EXECUTION"
          value="DISABLED"
          valueColor="#FFD700"
        />
      </View>

      {/* NOTIFICATIONS */}

      <Text
        style={[
          styles.section,
          {
            color: theme.text,
          },
        ]}
      >
        NOTIFICATIONS
      </Text>

      <View
        style={[
          styles.panel,
          {
            borderColor: theme.primary,
            backgroundColor: theme.panel,
          },
        ]}
      >
        <SettingRow
          title="SIGNAL ALERTS"
          value="ENABLED"
          valueColor="#00FF88"
        />

        <SettingRow
          title="AI ANALYSIS ALERTS"
          value="ENABLED"
          valueColor="#00FF88"
        />

        <SettingRow
          title="MARKET ALERTS"
          value="ENABLED"
          valueColor="#00FF88"
        />
      </View>

      {/* ABOUT */}

      <Text
        style={[
          styles.section,
          {
            color: theme.text,
          },
        ]}
      >
        ABOUT
      </Text>

      <View
        style={[
          styles.panel,
          {
            borderColor: theme.primary,
            backgroundColor: theme.panel,
          },
        ]}
      >
        <Text
          style={[
            styles.aboutTitle,
            {
              color: theme.primary,
            },
          ]}
        >
          SAINT ULTRA™
        </Text>

        <Text
          style={[
            styles.aboutText,
            {
              marginBottom: 6,
              fontWeight: "700",
            },
          ]}
        >
          By EVANS KOENA MOKOATEDI
        </Text>

        <Text
          style={[
            styles.aboutText,
            {
              marginBottom: 14,
            },
          ]}
        >
          Evanskoena41@gmail.com
        </Text>

        <Text style={styles.aboutText}>
          AI-powered market signal intelligence designed to
          analyze live market conditions and present
          actionable signal information.
        </Text>

        <View style={styles.versionRow}>
          <Text style={styles.versionLabel}>
            APPLICATION
          </Text>

          <Text style={styles.versionValue}>
            SAINT ULTRA
          </Text>
        </View>

        <View style={styles.versionRow}>
          <Text style={styles.versionLabel}>
            MODE
          </Text>

          <Text
            style={[
              styles.versionValue,
              {
                color: theme.primary,
              },
            ]}
          >
            SIGNAL ONLY
          </Text>
        </View>

        <View style={styles.versionRow}>
          <Text style={styles.versionLabel}>
            VERSION
          </Text>

          <Text style={styles.versionValue}>
            1.0.0
          </Text>
        </View>
      </View>

      <Text style={styles.footer}>
        SAINT ULTRA • AI SIGNAL INTELLIGENCE
      </Text>
    </ScrollView>
  );
}

function SettingRow({
  title,
  value,
  valueColor,
}: {
  title: string;
  value: string;
  valueColor: string;
}) {
  return (
    <View style={styles.settingRow}>
      <Text style={styles.settingTitle}>
        {title}
      </Text>

      <Text
        style={[
          styles.settingValue,
          {
            color: valueColor,
          },
        ]}
      >
        {value}
      </Text>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
  },

  content: {
    paddingHorizontal: 20,
    paddingTop: 35,
    paddingBottom: 120,
  },

  title: {
    fontSize: 32,
    fontWeight: "900",
    letterSpacing: 2,
  },

  subtitle: {
    color: "#8FA3BF",
    fontSize: 12,
    fontWeight: "800",
    letterSpacing: 1.5,
    marginTop: 6,
    marginBottom: 25,
  },

  section: {
    fontSize: 20,
    fontWeight: "900",
    letterSpacing: 1,
    marginTop: 10,
    marginBottom: 14,
  },

  panel: {
    borderWidth: 1,
    borderRadius: 22,
    padding: 18,
    marginBottom: 22,
  },

  panelTitle: {
    fontSize: 15,
    fontWeight: "900",
    letterSpacing: 1,
  },

  panelDescription: {
    color: "#8FA3BF",
    fontSize: 12,
    lineHeight: 18,
    marginTop: 6,
    marginBottom: 16,
  },

  themeCard: {
    minHeight: 72,
    borderWidth: 1,
    borderRadius: 16,
    paddingHorizontal: 14,
    marginBottom: 10,
    flexDirection: "row",
    alignItems: "center",
  },

  themeIndicator: {
    width: 18,
    height: 18,
    borderRadius: 9,
    marginRight: 14,
  },

  themeInfo: {
    flex: 1,
  },

  themeName: {
    color: "#FFFFFF",
    fontSize: 15,
    fontWeight: "900",
  },

  themeDescription: {
    color: "#8095B0",
    fontSize: 11,
    marginTop: 4,
  },

  themeStatus: {
    fontSize: 9,
    fontWeight: "900",
    letterSpacing: 1,
  },

  settingRow: {
    minHeight: 48,
    flexDirection: "row",
    alignItems: "center",
    justifyContent: "space-between",
    borderBottomWidth: 1,
    borderBottomColor: "rgba(127,162,201,0.12)",
  },

  settingTitle: {
    color: "#D6E9FF",
    fontSize: 12,
    fontWeight: "800",
    letterSpacing: 0.8,
  },

  settingValue: {
    fontSize: 10,
    fontWeight: "900",
    letterSpacing: 1,
  },

  aboutTitle: {
    fontSize: 20,
    fontWeight: "900",
    letterSpacing: 1,
  },

  aboutText: {
    color: "#9DB9D8",
    fontSize: 12,
    lineHeight: 19,
    marginTop: 8,
    marginBottom: 18,
  },

  versionRow: {
    flexDirection: "row",
    justifyContent: "space-between",
    paddingVertical: 9,
    borderTopWidth: 1,
    borderTopColor: "rgba(127,162,201,0.12)",
  },

  versionLabel: {
    color: "#7187A4",
    fontSize: 10,
    fontWeight: "800",
    letterSpacing: 1,
  },

  versionValue: {
    color: "#D6E9FF",
    fontSize: 10,
    fontWeight: "900",
  },

  footer: {
    color: "#60748F",
    textAlign: "center",
    fontSize: 10,
    fontWeight: "800",
    letterSpacing: 1,
    marginTop: 8,
  },
});
