import re

class FRGenerator:
    def __init__(self):
        self.fr_templates = {
            'authentication': [
                "The system shall {action} for {actor}",
                "The system shall provide {feature} functionality",
                "The system shall validate {entity}",
                "The system shall handle {exception_case}"
            ],
            'data_management': [
                "The system shall store {entity} in {location}",
                "The system shall retrieve {entity} based on {criteria}",
                "The system shall update {entity} when {condition}",
                "The system shall delete {entity} when {condition}"
            ],
            'user_interface': [
                "The system shall display {interface_element} to {actor}",
                "The system shall provide {navigation} between {screens}",
                "The system shall validate {input} in {context}"
            ],
            'business_logic': [
                "The system shall process {business_entity} according to {rules}",
                "The system shall calculate {metric} based on {parameters}",
                "The system shall enforce {business_rule} for {context}"
            ]
        }
    
    def generate_requirements(self, use_case_elements, model_type='rule-based'):
        """
        Generate functional requirements from use case elements
        """
        requirements = []
        fr_id = 1
        
        # Generate requirements based on actors
        for actor in use_case_elements.get('actors', []):
            if self.is_user_actor(actor):
                requirements.extend(self.generate_user_requirements(actor, use_case_elements, fr_id))
                fr_id += 5
        
        # Generate requirements from main flow
        requirements.extend(self.generate_flow_requirements(
            use_case_elements.get('main_flow', []), 
            fr_id, 
            "Main Flow"
        ))
        fr_id += len(use_case_elements.get('main_flow', []))
        
        # Generate requirements from alternative flows
        requirements.extend(self.generate_flow_requirements(
            use_case_elements.get('alternative_flows', []), 
            fr_id, 
            "Alternative Flow"
        ))
        
        # Generate requirements from preconditions and postconditions
        requirements.extend(self.generate_condition_requirements(use_case_elements, fr_id + 10))
        
        return requirements
    
    def is_user_actor(self, actor):
        """Check if actor is a user type"""
        user_keywords = ['user', 'customer', 'admin', 'manager', 'operator']
        return any(keyword in actor.lower() for keyword in user_keywords)
    
    def generate_user_requirements(self, actor, use_case_elements, start_id):
        """Generate requirements specific to user actors"""
        requirements = []
        
        # Interface requirements
        requirements.append({
            'id': f"FR-{start_id:03d}",
            'title': f"{actor} Interface Access",
            'description': f"The system shall provide interface access for {actor}",
            'category': 'User Interface',
            'priority': 'High'
        })
        
        # Authentication requirements if applicable
        if any(keyword in use_case_elements.get('goal', '').lower() for keyword in ['login', 'authenticate', 'access']):
            requirements.append({
                'id': f"FR-{start_id+1:03d}",
                'title': f"{actor} Authentication",
                'description': f"The system shall authenticate {actor} credentials",
                'category': 'Security',
                'priority': 'High'
            })
        
        return requirements
    
    def generate_flow_requirements(self, flow_steps, start_id, flow_type):
        """Generate requirements from flow steps"""
        requirements = []
        
        for i, step in enumerate(flow_steps, start=start_id):
            # Extract action from step
            action = self.extract_action_from_step(step)
            
            requirements.append({
                'id': f"FR-{i:03d}",
                'title': f"{flow_type} Step {i-start_id+1}",
                'description': f"The system shall {action}",
                'category': self.categorize_step(step),
                'priority': 'Medium' if flow_type == 'Main Flow' else 'Low'
            })
        
        return requirements
    
    def generate_condition_requirements(self, use_case_elements, start_id):
        """Generate requirements from preconditions and postconditions"""
        requirements = []
        current_id = start_id
        
        # Precondition requirements
        for precondition in use_case_elements.get('preconditions', []):
            requirements.append({
                'id': f"FR-{current_id:03d}",
                'title': "System Precondition",
                'description': f"The system shall ensure that {precondition}",
                'category': 'System',
                'priority': 'High'
            })
            current_id += 1
        
        # Postcondition requirements
        for postcondition in use_case_elements.get('postconditions', []):
            requirements.append({
                'id': f"FR-{current_id:03d}",
                'title': "System Postcondition",
                'description': f"The system shall achieve {postcondition}",
                'category': 'System',
                'priority': 'High'
            })
            current_id += 1
        
        return requirements
    
    def extract_action_from_step(self, step):
        """Extract the main action from a flow step"""
        # Remove step numbers
        clean_step = re.sub(r'^\d+\.\s*', '', step)
        
        # Convert to system perspective
        if 'user' in clean_step.lower():
            clean_step = clean_step.replace('user', 'allow user to')
        
        return clean_step.lower()
    
    def categorize_step(self, step):
        """Categorize step based on content"""
        step_lower = step.lower()
        
        if any(word in step_lower for word in ['validate', 'verify', 'check']):
            return 'Validation'
        elif any(word in step_lower for word in ['display', 'show', 'present']):
            return 'User Interface'
        elif any(word in step_lower for word in ['store', 'save', 'retrieve', 'update']):
            return 'Data Management'
        elif any(word in step_lower for word in ['calculate', 'process', 'compute']):
            return 'Business Logic'
        else:
            return 'General'
    
    def generate_traceability_matrix(self, use_case_elements, functional_requirements):
        """Generate traceability matrix between use case and requirements"""
        matrix = []
        
        # Map requirements to use case elements
        for requirement in functional_requirements:
            # Simple mapping based on content analysis
            mapped_elements = []
            
            # Check against use case name
            if any(word in requirement['description'].lower() 
                   for word in use_case_elements.get('use_case_name', '').lower().split()):
                mapped_elements.append('Use Case Name')
            
            # Check against goal
            if any(word in requirement['description'].lower() 
                   for word in use_case_elements.get('goal', '').lower().split()):
                mapped_elements.append('Goal')
            
            # Check against actors
            for actor in use_case_elements.get('actors', []):
                if actor.lower() in requirement['description'].lower():
                    mapped_elements.append(f'Actor: {actor}')
            
            matrix.append({
                'requirement_id': requirement['id'],
                'requirement_title': requirement['title'],
                'mapped_elements': mapped_elements if mapped_elements else ['General System']
            })
        
        return matrix