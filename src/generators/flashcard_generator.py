"""Flashcard Generation Module"""
import json
from typing import Dict, List
from openai import OpenAI


class FlashcardGenerator:
    """Generates flashcards for studying key concepts"""
    
    def __init__(self, api_key: str, model: str = "gpt-4"):
        self.client = OpenAI(api_key=api_key)
        self.model = model
    
    def generate_flashcards(self, content: str, num_cards: int = 20) -> List[Dict]:
        """
        Generate flashcards from content
        
        Args:
            content: Source content
            num_cards: Number of flashcards to generate
            
        Returns:
            List of flashcard dictionaries
        """
        prompt = f"""Create {num_cards} flashcards from the following educational content.

Each flashcard should have:
- A clear, concise question on the front
- A detailed answer on the back
- Optional hints or mnemonics
- Difficulty level (easy, medium, hard)

Content:
{content[:3000]}

Respond in JSON format with an array of flashcard objects."""
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are an expert at creating effective study flashcards."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                response_format={"type": "json_object"}
            )
            
            result = json.loads(response.choices[0].message.content)
            flashcards = result.get('flashcards', [])
            
            # Ensure each flashcard has required fields
            for card in flashcards:
                if 'front' not in card:
                    card['front'] = card.get('question', '')
                if 'back' not in card:
                    card['back'] = card.get('answer', '')
                if 'difficulty' not in card:
                    card['difficulty'] = 'medium'
            
            return flashcards
        except Exception as e:
            print(f"Error generating flashcards: {e}")
            return []
    
    def generate_concept_flashcards(self, concept: str, details: str) -> List[Dict]:
        """
        Generate flashcards for a specific concept
        
        Args:
            concept: The concept name
            details: Details about the concept
            
        Returns:
            List of flashcard dictionaries
        """
        prompt = f"""Create 5 flashcards specifically about: {concept}

Use the following details:
{details[:1000]}

Create cards that cover:
1. Definition
2. Key characteristics
3. Applications or examples
4. Common mistakes
5. Related concepts

Respond in JSON format with an array of flashcard objects."""
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are an expert at creating targeted study flashcards."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                response_format={"type": "json_object"}
            )
            
            result = json.loads(response.choices[0].message.content)
            return result.get('flashcards', [])
        except Exception as e:
            print(f"Error generating concept flashcards: {e}")
            return []
    
    def export_flashcards(self, flashcards: List[Dict], output_path: str, format: str = 'json'):
        """
        Export flashcards to a file
        
        Args:
            flashcards: List of flashcard dictionaries
            output_path: Path to save the flashcards
            format: Output format (json, txt, csv)
        """
        if format == 'json':
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump({'flashcards': flashcards}, f, indent=2, ensure_ascii=False)
        
        elif format == 'txt':
            with open(output_path, 'w', encoding='utf-8') as f:
                for i, card in enumerate(flashcards, 1):
                    f.write(f"{'='*60}\n")
                    f.write(f"FLASHCARD {i}\n")
                    f.write(f"{'='*60}\n\n")
                    f.write(f"FRONT (Question):\n{card.get('front', card.get('question', ''))}\n\n")
                    f.write(f"BACK (Answer):\n{card.get('back', card.get('answer', ''))}\n\n")
                    if card.get('hint'):
                        f.write(f"HINT: {card['hint']}\n\n")
                    if card.get('difficulty'):
                        f.write(f"DIFFICULTY: {card['difficulty']}\n\n")
                    f.write("\n")
        
        elif format == 'csv':
            import csv
            with open(output_path, 'w', encoding='utf-8', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=['front', 'back', 'hint', 'difficulty'])
                writer.writeheader()
                for card in flashcards:
                    writer.writerow({
                        'front': card.get('front', card.get('question', '')),
                        'back': card.get('back', card.get('answer', '')),
                        'hint': card.get('hint', ''),
                        'difficulty': card.get('difficulty', 'medium')
                    })
    
    def create_spaced_repetition_schedule(self, flashcards: List[Dict]) -> Dict:
        """
        Create a spaced repetition study schedule
        
        Args:
            flashcards: List of flashcards
            
        Returns:
            Dictionary with study schedule
        """
        # Simple spaced repetition: group by difficulty
        schedule = {
            'day_1': [],
            'day_3': [],
            'day_7': [],
            'day_14': [],
            'day_30': []
        }
        
        for card in flashcards:
            difficulty = card.get('difficulty', 'medium')
            if difficulty == 'hard':
                # Hard cards need more frequent review
                schedule['day_1'].append(card)
                schedule['day_3'].append(card)
                schedule['day_7'].append(card)
            elif difficulty == 'medium':
                schedule['day_1'].append(card)
                schedule['day_7'].append(card)
                schedule['day_14'].append(card)
            else:  # easy
                schedule['day_1'].append(card)
                schedule['day_14'].append(card)
                schedule['day_30'].append(card)
        
        return schedule
