import uuid


def generate_unique(instance):

    while True:
        ref_id = uuid.uuid4().hex[:6].upper()
        is_exist = instance.__class__.objects.filter(referral_code=ref_id).exists()
        if not is_exist:
            print(ref_id)
            return ref_id
