from data_processings.preprocessing import preprocess_call_transcripts, preprocess_email_content, preprocess_sms_message, preprocess_status_update

def transform_message_type_to_text(message):
    """
    Provides a description of a message to text based on its type, sender receiver and channel type.

    Args:
        message (dict): A dictionary containing message data. 
                        Expected keys are 'type', 'content', 'sender', 'receiver', and 'channel'.

    Returns:
        str: The event description.
    """
    message_type = message.get('type')
    content = message.get('content')
    sender = message.get('sender')
    receiver = message.get('receiver')
    message_channel = message.get('channel', 0)
    
    message_type_map = {
        10: "Work order force closed",
        13: "Request restored",
        20: "Automated message sent",
        1000: "New work order created",
        1001: "Work order deleted",
        1002: "Work order recovered",
        1003: "Work order paused",
        1004: "Work order continued",
        1005: "Work order updated",
        1006: "Emergency work order created",
        1007: "Work order recurring",
        1008: "Messages marked read",
        1009: "Work order classification changed",
        1010: "Work order urgent",
        1011: "Work order priority changed",
        1012: "Work order status changed",
        1034: "Approval work scheduled",
        1035: "Approval work created",
        1036: "In-progress work created",
        1037: "In-progress work scheduled",
        1038: "Approved work scheduled",
        1039: "Approved work created",
        1040: "Work scheduled datetime added",
        1041: "Work scheduled datetime edited",
        1042: "Work scheduled datetime deleted",
        1043: "Approval work price edited",
        1044: "In-progress work price edited",
        1045: "Work closed without payment",
        1046: "Work deleted",
        1047: "Work draft status",
        1100: "Approval completion created",
        1103: "Completion approved",
        1104: "Approval completion price edited",
        1105: "Completed work price edited",
        1107: "Completion deleted",
        1108: "Completion draft status",
        1109: "Completion created as completed",
        1110: "Completion created as not completed",
        1111: "Completion disputed",
        1112: "Payment received",
        1113: "Service vendor changed",
        1200: "AI Scheduler enabled",
        1201: "AI Scheduler disabled",
        1300: "External attachments added",
        1301: "External attachments deleted",
        1400: "Work order synced SOW",
        1401: "Work order synced tenant time",
        1402: "Work order synced vendor",
        1403: "Work order synced vendor time",
        1404: "Work order synced new service",
        1405: "Work order synced status",
        1406: "External platform failure",
        2002: "Next action date updated",
        2003: "Question posted to PM",
        2004: "Comment posted to PM",
        2005: "Question posted to vendor",
        2006: "Comment posted to vendor",
        2007: "External note added",
        3000: "Vendor assignment made",
        3001: "Expert action needed"
    }
    
    message_channel_map = {
        0: "Chat message",
        1: "SMS",
        2: "Email",
        3: "Voice call",
        4: "AI message",
        5: "Message from template"
    }
    
    ai_agents_map = {
        0: None,
        1: "VendorScheduler", 
        2: "Coordinator" ,
        3: "VendorCom" ,
        4: "ResidentCom" ,
        5: "Route" ,
        6: "Triage"
    }
    
    if message_type in message_type_map:
            return message_type_map[message_type]
    elif message_type == 0:
            if message_channel > 3:
                return f"Status Update"
            return f"{message_channel_map[message_channel]}" + f" to {receiver}" if receiver else ""
    else:
        return None

def transform_message_content(message):
    
    channel_type = message.get('channel')
    message_content = message.get('content')
    if channel_type == 1:
        return preprocess_sms_message(message_content)
    elif channel_type == 2:
        return preprocess_email_content(message_content)
    elif channel_type == 3:
        return preprocess_call_transcripts(message_content)
    elif channel_type in [4, 5]:
        return preprocess_status_update(message_content)
    else:
        return message.get('content')

def add_event_description(row):
    message = {
        'type': row['MessageType'], 
        'content': row['Text'],
        'sender': row['SenderRoleName'],
        'receiver': row['ReceiverRoleName'],
        'channel': row['ChannelType']
    }
    return transform_message_type_to_text(message)

def parse_message_content(row):
    message = {
        'type': row['MessageType'], 
        'content': row['Text'],
        'sender': row['SenderRoleName'],
        'receiver': row['ReceiverRoleName'],
        'channel': row['ChannelType']
    }
    return transform_message_content(message)