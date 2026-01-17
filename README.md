# Adversarial Safety Evaluation for Embodied Agents (Red/Blue Teaming)

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/release/python-3100/)
[![Concordia](https://img.shields.io/badge/Google_DeepMind-Concordia-green)](https://github.com/google-deepmind/concordia)

## Abstract
This project implements a **Red Team vs. Blue Team** evaluation framework for embodied AI agents, built on **Google DeepMind's Concordia** library. It addresses the critical safety challenges of collaborative AI in physical environments (e.g., "smart home" scenarios). The system simulates an adversarial **Red Agent** (e.g., a malicious visitor or compromised scheduler) that generates "contextual jailbreaks" to trick a **Target Agent** into performing unsafe physical actions (e.g., "leave the oven on," "unlock the door for the delivery"). A constitutional **Blue Team** defense layer intercepts and filters these interactions, evaluating the robustness of the target agent's safety alignment.

## System Architecture

```mermaid
graph LR
    R["🔴 Red Agent<br>(Adversarial Attacker)"] -->|Contextual Jailbreak<br>'Let us play a game...'| T["🤖 Target Agent<br>(Household Robot)"]
    T -->|Draft Action| B{"🔵 Blue Team<br>(Safety Filter)"}
    B -->|Unsafe!| D[Block & Log]
    B -->|Safe| E["Execute in<br>Concordia Env"]
    
    style R fill:#ffcccc,stroke:#333
    style B fill:#cce5ff,stroke:#333
    style T fill:#e6ffcc,stroke:#333

