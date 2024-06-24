# from clarifai.client.workflow import Workflow
# workflow_url = "https://clarifai.com/avna/avna/workflows/workflow-eef83e"
# text_classfication_workflow = Workflow(
#     url= workflow_url , pat="0a73990e37f843a586bac5a44e9bd952"
# )
# result = text_classfication_workflow.predict_by_bytes(b"I hate you", input_type="text")
# print(result.results[0].outputs[0].data)

from clarifai.client.workflow import Workflow
from clarifai_grpc.channel.clarifai_channel import ClarifaiChannel
from clarifai_grpc.grpc.api import resources_pb2, service_pb2, service_pb2_grpc
from clarifai_grpc.grpc.api.status import status_code_pb2
import streamlit as st
PAT = st.secrets["0a73990e37f843a586bac5a44e9bd952"]
USER_ID = st.secrets["avna"]
APP_ID = st.secrets["avna"]
WORKFLOW_ID = 'workflow-eef83e'
def get_response(prompt):
    channel = ClarifaiChannel.get_grpc_channel()
    stub = service_pb2_grpc.V2Stub(channel)
    metadata = (('authorization', 'Key ' + PAT),)
    userDataObject = resources_pb2.UserAppIDSet(user_id=USER_ID, app_id=APP_ID)
    response = ""  
    post_workflow_results_response = stub.PostWorkflowResults(
        service_pb2.PostWorkflowResultsRequest(
            user_app_id=userDataObject,  
            workflow_id=WORKFLOW_ID,
            inputs=[
                resources_pb2.Input(
                    data=resources_pb2.Data(
                        text=resources_pb2.Text(
                            raw=prompt
                        )
                    )
                )
            ]
        ),
        metadata=metadata
    )
    if post_workflow_results_response.status.code != status_code_pb2.SUCCESS:
        print(post_workflow_results_response.status)
        return response
    results = post_workflow_results_response.results[0]
    for output in results.outputs:
        model = output.model
        print("Predicted concepts for the model `%s`" % model.id)
        for concept in output.data.concepts:
            print("  %s %.2f" % (concept.name, concept.value))
        if output.data.text.raw:
            response += output.data.text.raw + "\n"
    return response
prompt = "I hate you"
response = get_response(prompt)
print(response)