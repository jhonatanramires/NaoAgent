#!/usr/bin/env python3

"""
Basic example of edge_tts usage.
"""

import asyncio
import sys
import edge_tts

VOICE = "es-BO-SofiaNeural"
OUTPUT_FILE = 'C:\\Users\\Windows 10\\Desktop\\NaoAgent\\TextToSpeech\\test.mp3'


async def amain(text) -> None:
    """Main function"""
    communicate = edge_tts.Communicate(text, VOICE)
    await communicate.save(OUTPUT_FILE)