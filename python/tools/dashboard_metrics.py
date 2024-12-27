from python.helpers.tool import Tool, Response
from python.helpers.memory import Memory

class DashboardMetrics(Tool):
    """Tool for handling dashboard metrics and interactions"""

    async def execute(self, section="", action="", data={}, **kwargs):
        """
Process dashboard metrics and interactions

Args:
section (str): Dashboard section (discover, space, flow)
action (str): Type of action performed
data (dict): Additional metric data
"""
        db = await Memory.get(self.agent)
        
        # Store the interaction/metric data
        metric_data = {
            "timestamp": data.get("timestamp"),
            "section": section,
            "action": action,
            "metrics": data.get("metrics", {}),
            "context": self.agent.context
        }
        
        await db.add_document(metric_data)

        result = self.agent.read_prompt(
            "fw.dashboard_metric.md",
            section=section,
            action=action
        )
        
        return Response(message=result, break_loop=False)