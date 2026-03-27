from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from backend.database import get_db
from backend.src.auth.dependencies import get_current_user, get_current_admin
from backend.src.auth.model import User
from backend.src.category.schemas import CategoryCreate, CategoryResponse, CategoryUpdate
from backend.src.category.service import create_category, get_categories, get_category_by_id, update_category, delete_category

router = APIRouter(prefix="/categories", tags=["categories"])


@router.post("/create", response_model=CategoryResponse)
async def create_category_endpoint(
    data: CategoryCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_admin),
):
    category = await create_category(db, data)
    return category


@router.get("/", response_model=list[CategoryResponse])
async def get_categories_endpoint(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return await get_categories(db)


@router.get("/{category_id}", response_model=CategoryResponse)
async def get_category_endpoint(
    category_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    category = await get_category_by_id(db, category_id)
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found",
        )
    return category

@router.patch("/{category_id}", response_model=CategoryResponse)
async def update_category_endpoint(
    category_id: int,
    data: CategoryUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_admin)
):
    category = await update_category(db, category_id, data)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return category

@router.delete("/{category_id}", status_code=204)
async def delete_category_endpoint(
    category_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_admin),
):
    deleted = await delete_category(db, category_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Category not found")

