import re
import nltk
import ssl

try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_unverified_https_context = _create_unverified_https_context

# Download required NLTK data
def download_nltk_data():
    try:
        nltk.data.find('tokenizers/punkt')
    except LookupError:
        print("Downloading NLTK punkt tokenizer...")
        nltk.download('punkt', quiet=True)
    
    try:
        nltk.data.find('taggers/averaged_perceptron_tagger')
    except LookupError:
        print("Downloading NLTK POS tagger...")
        nltk.download('averaged_perceptron_tagger', quiet=True)

# Download data on import
download_nltk_data()

from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.tag import pos_tag

class NLPProcessor:
    def __init__(self):
        self.use_case_patterns = {
            'actors': [
                r'actor[s]?[:]?\s*(.*?)(?:\n\n|$)',
                r'primary.*?actor[:]?\s*(.*?)\n',
                r'secondary.*?actor[:]?\s*(.*?)\n',
                r'user[s]?[:]?\s*(.*?)(?:\n\n|$)'
            ],
            'goals': [
                r'goal[s]?[:]?\s*(.*?)(?:\n\n|$)',
                r'purpose[s]?[:]?\s*(.*?)(?:\n\n|$)',
                r'objective[s]?[:]?\s*(.*?)(?:\n\n|$)'
            ],
            'preconditions': [
                r'precondition[s]?[:]?\s*(.*?)(?:\n\n|$)',
                r'assumption[s]?[:]?\s*(.*?)(?:\n\n|$)',
                r'prerequisite[s]?[:]?\s*(.*?)(?:\n\n|$)'
            ],
            'main_flow': [
                r'main.*?flow[:]?\s*(.*?)(?:\n\n|$)',
                r'basic.*?flow[:]?\s*(.*?)(?:\n\n|$)',
                r'normal.*?flow[:]?\s*(.*?)(?:\n\n|$)',
                r'steps[:]?\s*(.*?)(?:\n\n|$)'
            ],
            'alternative_flows': [
                r'alternative.*?flow[s]?[:]?\s*(.*?)(?:\n\n|$)',
                r'exception[s]?[:]?\s*(.*?)(?:\n\n|$)',
                r'error.*?flow[s]?[:]?\s*(.*?)(?:\n\n|$)'
            ],
            'postconditions': [
                r'postcondition[s]?[:]?\s*(.*?)(?:\n\n|$)',
                r'result[s]?[:]?\s*(.*?)(?:\n\n|$)',
                r'outcome[s]?[:]?\s*(.*?)(?:\n\n|$)'
            ]
        }
    
    def extract_use_case_elements(self, text):
        """
        Extract use case elements from text using NLP and pattern matching
        """
        elements = {
            'use_case_name': self.extract_use_case_name(text),
            'actors': self.extract_actors(text),
            'goal': self.extract_goal(text),
            'preconditions': self.extract_preconditions(text),
            'main_flow': self.extract_main_flow(text),
            'alternative_flows': self.extract_alternative_flows(text),
            'postconditions': self.extract_postconditions(text)
        }
        
        return elements
    
    def extract_use_case_name(self, text):
        """Extract use case name"""
        patterns = [
            r'use case[:]?\s*["\']?(.*?)["\']?(?:\n|$)',
            r'use case name[:]?\s*["\']?(.*?)["\']?(?:\n|$)',
            r'system[:]?\s*["\']?(.*?)\s*use case',
            r'^["\']?(.*?use case.*?)["\']?(?:\n|$)'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                name = match.group(1).strip()
                if name and name.lower() != "use case":
                    return name
        
        # If no pattern matches, use first line as use case name
        lines = text.split('\n')
        first_line = lines[0].strip() if lines else "Unknown Use Case"
        return first_line if first_line and len(first_line) < 100 else "Unknown Use Case"
    
    def extract_actors(self, text):
        """Extract actors from text"""
        actors = []
        
        for pattern in self.use_case_patterns['actors']:
            matches = re.findall(pattern, text, re.IGNORECASE | re.DOTALL)
            for match in matches:
                if isinstance(match, tuple):
                    match = match[0]
                if match:
                    # Split by commas, bullets, or newlines
                    actor_list = re.split(r'[,•\-\n]', match)
                    for actor in actor_list:
                        actor_clean = actor.strip()
                        if actor_clean and len(actor_clean) < 50:  # Sanity check
                            actors.append(actor_clean)
        
        return list(set(actors)) if actors else ['User', 'System']
    
    def extract_goal(self, text):
        """Extract goal from text"""
        for pattern in self.use_case_patterns['goals']:
            match = re.search(pattern, text, re.IGNORECASE | re.DOTALL)
            if match:
                goal = match.group(1).strip()
                if goal:
                    return goal
        
        return "Enable system functionality"
    
    def extract_preconditions(self, text):
        """Extract preconditions"""
        return self._extract_list_items(text, 'preconditions')
    
    def extract_main_flow(self, text):
        """Extract main flow steps"""
        steps = self._extract_flow_steps(text, 'main_flow')
        return steps if steps else ["1. User accesses the system", "2. System processes request", "3. System provides response"]
    
    def extract_alternative_flows(self, text):
        """Extract alternative flows"""
        return self._extract_list_items(text, 'alternative_flows')
    
    def extract_postconditions(self, text):
        """Extract postconditions"""
        return self._extract_list_items(text, 'postconditions')
    
    def _extract_list_items(self, text, element_type):
        """Extract list items for various elements"""
        items = []
        
        # Look for bullet points or numbered lists
        bullet_pattern = r'[•\-\*]\s*(.*?)(?=\n|$)'
        numbered_pattern = r'\d+\.\s*(.*?)(?=\n|$)'
        
        # First try to find specific section
        section_patterns = self.use_case_patterns.get(element_type, [])
        for pattern in section_patterns:
            section_match = re.search(pattern, text, re.IGNORECASE | re.DOTALL)
            if section_match:
                section_text = section_match.group(1)
                # Extract items from the section
                bullets = re.findall(bullet_pattern, section_text)
                numbers = re.findall(numbered_pattern, section_text)
                items.extend(bullets + numbers)
                break
        
        # If no specific section found, look throughout text
        if not items:
            all_bullets = re.findall(bullet_pattern, text)
            all_numbers = re.findall(numbered_pattern, text)
            items = all_bullets + all_numbers
        
        # Clean and filter items
        cleaned_items = [item.strip() for item in items if item.strip() and len(item.strip()) < 200]
        return cleaned_items[:10]  # Limit to 10 items
    
    def _extract_flow_steps(self, text, element_type):
        """Extract flow steps with sequence numbers"""
        steps = []
        
        # Look for numbered steps (1., 2., etc.)
        numbered_pattern = r'(\d+)\.\s*(.*?)(?=\n\d+\.|\n\n|$)'
        matches = re.findall(numbered_pattern, text)
        
        for number, step in matches:
            if step.strip():
                steps.append(f"{number}. {step.strip()}")
        
        return steps if steps else self._extract_simple_steps(text)
    
    def _extract_simple_steps(self, text):
        """Extract steps from simple text"""
        sentences = sent_tokenize(text)
        steps = []
        for i, sentence in enumerate(sentences[:5], 1):  # Limit to 5 steps
            steps.append(f"{i}. {sentence.strip()}")
        return steps