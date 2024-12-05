from utils import *
import time

slot_questions = fetch_questions()

if slot_questions.get("error",None) is not None:
    print("Error while fetching questions")


# initialize slots


user_response = "start"

not_answered = get_all_qid(slot_questions)

q_id = not_answered[0]
# Dictionary to store responses
responses = []



while len(not_answered) > 0:
    # Fill slots of question and option
    ques, options, rule, validations = create_question(q_id, slot_questions)

    valid_responses = []
    print(ques)
    if options:
        valid_responses = [value for op in options for value in (op.get("payload"), op.get("title"))]
        for option in options:
            print("o ", option.get("title"))

    user_response = input("user: ")
    try:
        user_response = int(user_response)
    except ValueError:
        pass 
    
    # Validate user response
    if user_response == "cancel":
        print("Thanks for your feedback")
        break  # Exit the loop gracefully

    if len(valid_responses) > 0:
        if user_response not in valid_responses:
            
            print("Enter a valid response")
            continue  # Prompt the user again without proceeding further

    # check given validations in questions

    is_validated = check_validation(validations)

    if not is_validated:
        print("Enter a valid response")
        continue


    # Map user response to text option
    response_text = None
    if options:
        for option in options:
            if user_response in (option.get("payload"), option.get("title")):
                response_text = option.get("title")
                break
        
    # Store the response
    responses.append({
        "question_id": q_id,
        "user_response": user_response,
        "response_text": response_text
    })

    # Remove the current question from not_answered
    if q_id in not_answered:
        not_answered.remove(q_id)

    # Handle rules and determine the next question
    if rule is None:
        if len(not_answered) > 0:
            q_id = not_answered[0]
    else:
        hidden_ques = get_hidden_question_ids(rule)
        for ques in hidden_ques:
            if ques in not_answered:
                not_answered.remove(ques)

        next_question = get_next_question(rule, {"input": user_response})

        if len(next_question) == 0 and len(not_answered) > 0:
            q_id = not_answered[0]
        elif len(next_question) > 0:
            q_id = next_question[0]

print("Question remaining" ,not_answered)
# Final message
if len(not_answered) == 0:
    print("Thanks for your feedback")

# Print all responses
print("\nUser Responses:")
for response in responses:
    print(f"Question ID: {response['question_id']}, User Response: {response['user_response']}, Response Text: {response['response_text']}")



import time

def time_wrapper(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()  
        result = func(*args, **kwargs)
        end_time = time.time()  
        execution_time = end_time - start_time 
        print(f"Execution time of {func.__name__}: {execution_time:.4f} s")
        return result
    return wrapper

#
# @time_wrapper
# def example_function(n):
#     total = 0
#     for i in range(n):
#         total += i
#     return total

# result = example_function(1000000)