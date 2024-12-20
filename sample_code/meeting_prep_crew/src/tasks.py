from textwrap import dedent
from crewai import Task


class MeetingPrepTasks:

    def research_task(self, agent, meeting_participants, meeting_context):
        return Task(
            description=f"""
                Conduct comprehensive research on each of the individuals and companies
                involved in the upcoming meeting. Gather information on recent
                news, achievements, professional background, and any relevant
                business activities.

                Participants: {meeting_participants}
                Meeting Context: {meeting_context}""",
            expected_output="""\
                    A detailed report summarizing key findings about each participant
                    and company, highlighting information that could be relevant for the meeting.""",
                    
        )
