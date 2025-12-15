"""Quiz Generation Module"""
import json
from typing import Dict, List
from openai import OpenAI


class QuizGenerator:
    """Generates quizzes and assessments for modules"""
    
    def __init__(self, api_key: str, model: str = "gpt-4"):
        self.client = OpenAI(api_key=api_key)
        self.model = model
    
    def generate_quiz(self, content: str, num_questions: int = 10,
                     question_types: List[str] = None) -> Dict:
        """
        Generate a quiz from content
        
        Args:
            content: Source content
            num_questions: Number of questions
            question_types: Types of questions (multiple_choice, true_false, short_answer)
            
        Returns:
            Dictionary containing quiz questions
        """
        if question_types is None:
            question_types = ['multiple_choice', 'true_false', 'short_answer']
        
        prompt = f"""Create a {num_questions}-question quiz from the following content.

Include a mix of:
- Multiple choice questions (4 options each)
- True/False questions
- Short answer questions

Content:
{content[:3000]}

For each question provide:
- Question text
- Question type
- Options (for multiple choice)
- Correct answer
- Explanation of the correct answer
- Points value (based on difficulty)

Respond in JSON format with a quiz object containing an array of questions."""
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are an expert educator creating effective assessment quizzes."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                response_format={"type": "json_object"}
            )
            
            result = json.loads(response.choices[0].message.content)
            quiz = result.get('quiz', result)
            
            # Ensure quiz has required structure
            if 'questions' not in quiz:
                quiz = {'questions': result.get('questions', [])}
            
            quiz['total_points'] = sum(q.get('points', 1) for q in quiz['questions'])
            quiz['num_questions'] = len(quiz['questions'])
            
            return quiz
        except Exception as e:
            print(f"Error generating quiz: {e}")
            return {'questions': [], 'total_points': 0, 'num_questions': 0}
    
    def generate_module_quiz(self, module: Dict, difficulty: str = 'mixed') -> Dict:
        """
        Generate a quiz specifically for a module
        
        Args:
            module: Module dictionary
            difficulty: Quiz difficulty (easy, medium, hard, mixed)
            
        Returns:
            Quiz dictionary
        """
        # Extract content from module
        content = module.get('introduction', '')
        for section in module.get('sections', []):
            if isinstance(section, dict):
                content += ' ' + section.get('content', '')
        
        prompt = f"""Create a comprehensive quiz for the module: {module.get('title', 'Module')}

Learning objectives:
{json.dumps(module.get('learning_objectives', []))}

Difficulty level: {difficulty}

Create 8-12 questions that:
1. Test understanding of learning objectives
2. Cover key concepts from the module
3. Include various question types
4. Are appropriate for the difficulty level

Content excerpt:
{content[:2000]}

Respond in JSON format."""
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are an expert at creating module assessments."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                response_format={"type": "json_object"}
            )
            
            result = json.loads(response.choices[0].message.content)
            quiz = result.get('quiz', result)
            
            if 'questions' not in quiz:
                quiz = {'questions': result.get('questions', [])}
            
            quiz['module_name'] = module.get('title', module.get('module_name', ''))
            quiz['module_number'] = module.get('module_number', 1)
            quiz['total_points'] = sum(q.get('points', 1) for q in quiz['questions'])
            
            return quiz
        except Exception as e:
            print(f"Error generating module quiz: {e}")
            return {'questions': [], 'module_name': '', 'total_points': 0}
    
    def export_quiz(self, quiz: Dict, output_path: str, format: str = 'json'):
        """
        Export quiz to a file
        
        Args:
            quiz: Quiz dictionary
            output_path: Path to save the quiz
            format: Output format (json, txt)
        """
        if format == 'json':
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(quiz, f, indent=2, ensure_ascii=False)
        
        elif format == 'txt':
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write("="*60 + "\n")
                if quiz.get('module_name'):
                    f.write(f"QUIZ: {quiz['module_name']}\n")
                else:
                    f.write("QUIZ\n")
                f.write("="*60 + "\n\n")
                
                f.write(f"Total Questions: {quiz.get('num_questions', len(quiz.get('questions', [])))}\n")
                f.write(f"Total Points: {quiz.get('total_points', 0)}\n\n")
                
                for i, question in enumerate(quiz.get('questions', []), 1):
                    f.write(f"\n{'='*60}\n")
                    f.write(f"QUESTION {i} ({question.get('points', 1)} points)\n")
                    f.write(f"{'='*60}\n\n")
                    
                    f.write(f"{question.get('question', '')}\n\n")
                    
                    q_type = question.get('type', question.get('question_type', 'unknown'))
                    f.write(f"Type: {q_type}\n\n")
                    
                    if q_type == 'multiple_choice' and question.get('options'):
                        f.write("Options:\n")
                        for opt_idx, option in enumerate(question['options'], 1):
                            f.write(f"  {chr(64+opt_idx)}. {option}\n")
                        f.write("\n")
                    
                    f.write(f"Correct Answer: {question.get('correct_answer', question.get('answer', ''))}\n\n")
                    
                    if question.get('explanation'):
                        f.write(f"Explanation: {question['explanation']}\n\n")
    
    def grade_quiz(self, quiz: Dict, answers: Dict[int, str]) -> Dict:
        """
        Grade a quiz based on provided answers
        
        Args:
            quiz: Quiz dictionary
            answers: Dictionary mapping question number to answer
            
        Returns:
            Grading results
        """
        results = {
            'total_questions': len(quiz.get('questions', [])),
            'correct': 0,
            'incorrect': 0,
            'score': 0,
            'max_score': quiz.get('total_points', 0),
            'percentage': 0,
            'details': []
        }
        
        for i, question in enumerate(quiz.get('questions', []), 1):
            correct_answer = question.get('correct_answer', question.get('answer', ''))
            user_answer = answers.get(i, '')
            
            is_correct = str(user_answer).strip().lower() == str(correct_answer).strip().lower()
            
            if is_correct:
                results['correct'] += 1
                results['score'] += question.get('points', 1)
            else:
                results['incorrect'] += 1
            
            results['details'].append({
                'question_number': i,
                'correct': is_correct,
                'user_answer': user_answer,
                'correct_answer': correct_answer,
                'points_earned': question.get('points', 1) if is_correct else 0
            })
        
        if results['max_score'] > 0:
            results['percentage'] = (results['score'] / results['max_score']) * 100
        
        return results
