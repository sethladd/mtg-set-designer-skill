# MTG Card Maker — Sources

## Card Frame Assets

- M15+ card frame images (W, U, B, R, G, M, C) and power/toughness box overlays sourced from the Card Conjurer assets repository:
  https://github.com/2gnc/cardconjurer-assets/tree/main/assets/mtg/frame/m15/regular

- Card Conjurer project (original tool these assets support):
  https://github.com/joshbirnholz/cardconjurer

## Card Layout Measurements

- Arcmage wiki template references (53 x 39 mm art, 53 x 24 mm text)
- Draftsim / Cardboard Keeper card measurement guides
- MTG Wiki illustration dimensions

## Mana Symbols

- andrewgioia/mana project (SVG mana and tap symbols):
  https://github.com/andrewgioia/mana

## Art Generation (Gemini Nano Banana)

- Gemini API — Nano Banana image generation (model IDs, aspect ratios, image_config options, multimodal response parts):
  https://ai.google.dev/gemini-api/docs/image-generation

- google-genai Python SDK (client.models.generate_content, types.GenerateContentConfig, types.ImageConfig, part.inline_data):
  https://github.com/googleapis/python-genai

- Google AI Studio — API key provisioning:
  https://aistudio.google.com/app/apikey

- Vertex AI — Generate and edit images overview (context on Imagen → Nano Banana migration):
  https://docs.cloud.google.com/vertex-ai/generative-ai/docs/image/overview

## Card Art Box Geometry

- M15+ frame art window is 53 × 39 mm (aspect ratio ≈ 1.359:1). Nano
  Banana's closest landscape option is 4:3 (1.333:1); the difference is
  trimmed top/bottom in `scripts/generate_art.py:crop_to_art_box`.
