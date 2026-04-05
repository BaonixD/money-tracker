import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { ApiService } from '../../core/api';
import { Category } from '../../shared/models/category.model';

@Component({
  selector: 'app-category-list',
  imports: [CommonModule, FormsModule],
  templateUrl: './category-list.html',
  styleUrl: './category-list.scss',
})
export class CategoryList implements OnInit {
  categories: Category[] = [];
  newCategoryName = '';

  constructor(private api: ApiService) {}

  ngOnInit() {
    this.loadCategories();
  }

  loadCategories() {
    this.api.getCategories().subscribe((data) => {
      this.categories = data;
    });
  }

  addCategory() {
    if (!this.newCategoryName.trim()) return;
    this.api.createCategory({ name: this.newCategoryName.trim() }).subscribe(() => {
      this.newCategoryName = '';
      this.loadCategories();
    });
  }

  deleteCategory(id: number) {
    this.api.deleteCategory(id).subscribe(() => {
      this.loadCategories();
    });
  }
}
