# --- File: agents/views.py ---
# Views for listing agents and simulating agent invocation.
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Agent
from .serializers import AgentSerializer
import random
import uuid

class AgentViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Agent.objects.filter(is_active=True)
    serializer_class = AgentSerializer
    permission_classes = [IsAuthenticated] # Users must be authenticated to view agents

    @action(detail=True, methods=['post'])
    def invoke(self, request, pk=None):
        """
        Simulates the invocation of an AI agent.
        For MVP, this returns a predefined or dummy AI-generated text.
        """
        try:
            agent = self.get_object() # Get the specific agent instance
        except Agent.DoesNotExist:
            return Response({'detail': 'Agent not found.'}, status=status.HTTP_404_NOT_FOUND)

        user_input = request.data.get('input', '') # Get input from the frontend

        # --- SIMULATED AI LOGIC FOR MVP ---
        # In a real application, you would call an external LLM API here.
        # Example:
        # from your_ai_library import get_ai_response
        # ai_response = get_ai_response(agent.name, user_input)

        predefined_responses = [
            f"Thank you for invoking the '{agent.name}' agent! Your request '{user_input}' has been processed. Here is a simulated AI response: 'Leveraging cutting-edge algorithms, your query reveals deep insights into data synthesis and strategic optimization.'",
            f"The '{agent.name}' agent is now active. Input received: '{user_input}'. Simulated output: 'Our advanced neural network predicts a 20% increase in efficiency through intelligent automation.'",
            f"Query for '{agent.name}' agent: '{user_input}'. Response: 'After comprehensive analysis, the system recommends a dynamic recalibration of your workflow for maximum throughput.'",
            f"Executing '{agent.name}' with input '{user_input}'. Simulated result: 'The agent has generated a compelling content piece that addresses your core objectives, focusing on user engagement metrics and conversion funnels.'",
            f"The '{agent.name}' agent, with your input '{user_input}', has concluded its task. Here's a summary of its findings: 'Strategic positioning in the market requires an agile approach to resource allocation and a robust framework for continuous innovation.'"
        ]

        # Select a random response
        simulated_ai_response = random.choice(predefined_responses) + f" (Simulated ID: {uuid.uuid4().hex})"

        return Response({
            'agent_id': agent.id,
            'agent_name': agent.name,
            'user_input': user_input,
            'ai_response': simulated_ai_response,
            'status': 'success'
        }, status=status.HTTP_200_OK)


