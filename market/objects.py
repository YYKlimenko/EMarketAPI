from fastapi import Depends

from auth.permissions import permit_for_admin, permit_for_owner
from market.permissions import (permit_for_user, permit_get_order_for_owner,
                                permit_post_order_for_owner)

PERMIT_GET_ORDER_FOR_OWNER = Depends(permit_get_order_for_owner)
PERMIT_POST_ORDER_FOR_OWNER = Depends(permit_post_order_for_owner)
PERMIT_FOR_USER = Depends(permit_for_user)
PERMIT_FOR_OWNER = Depends(permit_for_owner)
PERMIT_FOR_ADMIN = Depends(permit_for_admin)
