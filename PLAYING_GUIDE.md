# Temple Run AI - Player's Guide

Welcome to the **Gesture-Controlled Temple Run** experience! This guide explains how to pilot your character using only hand movements and Computer Vision.

## The Setup (The "Cockpit")

Computer Vision relies on seeing your hand clearly. Follow these steps for the best experience:

1.  **Lighting:** Ensure your hand is well-lit. Avoid strong backlighting (like a bright window behind you).
2.  **Distance:** Sit about **2-3 feet (60-90 cm)** away from the webcam.
3.  **Position:** Your hand should be visible in the **center** of the camera frame when you are resting.
4.  **The "Focus" Trick:**
    - Run the Python script.
    - **Click once inside the game browser window.**
    - _Note: If you don't click the game, the key presses will be sent to your terminal instead of the runner!_

---

## The "Neutral" Stance

**Crucial:** When you are running straight, keep your hand in the **Center Zone** (between the two vertical lines on screen).

- **Rest Position:** Keep your hand in a "relaxed claw" or loose fist.
- **Why?**
  - Fully Open Hand = **JUMP**
  - Tight Fist = **SLIDE**
  - Relaxed Hand = **RUN**

---

## Controls & Moves

| Action         | The Gesture                                                                                     | Visual Cue on Screen |
| :------------- | :---------------------------------------------------------------------------------------------- | :------------------- |
| **TURN LEFT**  | Move your **entire hand** physically to the **Left Edge** of the screen (past the yellow line). | Text: `LEFT`         |
| **TURN RIGHT** | Move your **entire hand** physically to the **Right Edge** of the screen.                       | Text: `RIGHT`        |
| **JUMP**       | **Open your hand wide** (Show all 5 fingers). Think "High Five!" 🖐️                             | Text: `JUMP`         |
| **SLIDE**      | **Make a Fist** (Fold all fingers). ✊                                                          | Text: `SLIDE`        |

---

## Pro Strategies

### 1. The "Snap Back" Technique

When turning corners, don't leave your hand on the edge!

1.  Move hand Left/Right to turn.
2.  **Immediately snap back to Center.**
    - _Why?_ If you linger in the turn zone, the game might register a second turn and run you into a wall.

### 2. The Jump-Slide Rhythm

The camera needs to see the difference between "Jump" and "Run."

- **Wrong:** Keeping your hand open constantly.
- **Right:** Open (Jump) ➔ Relax (Run) ➔ Fist (Slide) ➔ Relax (Run).

---

## Troubleshooting

| Problem                    | Solution                                                                                          |
| :------------------------- | :------------------------------------------------------------------------------------------------ |
| **"He won't turn!"**       | Check the camera window. Is your hand actually crossing the yellow line, or did it go off-screen? |
| **"The game ignores me!"** | You lost "Window Focus." Click the game screen with your mouse again.                             |
| **"He keeps Jumping!"**    | Your "Neutral" hand is too open. Curl your fingers slightly more when resting.                    |
| **"Input is laggy!"**      | Ensure your room is bright. Low light makes the webcam shutter slower, causing lag.               |

---

**Happy Running!**
