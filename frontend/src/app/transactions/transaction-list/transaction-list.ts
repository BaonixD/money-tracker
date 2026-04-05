import { Component, OnInit, ChangeDetectorRef } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { ApiService } from '../../core/api';
import { Transaction, TransactionCreate } from '../../shared/models/transaction.model';
import { Category } from '../../shared/models/category.model';

@Component({
  selector: 'app-transaction-list',
  imports: [CommonModule, FormsModule],
  templateUrl: './transaction-list.html',
  styleUrl: './transaction-list.scss',
})
export class TransactionList implements OnInit {
  transactions: Transaction[] = [];
  categories: Category[] = [];
  total = 0;
  limit = 20;
  offset = 0;

  // filters
  filterType: string = '';
  filterCategoryId: number | null = null;

  // new transaction form
  showForm = false;
  newTx: TransactionCreate = { amount: 0, description: '', type: 'expense', category_id: 0 };

  constructor(private api: ApiService, private cdr: ChangeDetectorRef) {}

  ngOnInit() {
    this.loadTransactions();
    this.api.getCategories().subscribe((data) => {
      this.categories = data;
    });
  }

  loadTransactions() {
    const params: any = { limit: this.limit, offset: this.offset };
    if (this.filterType) params.type = this.filterType;
    if (this.filterCategoryId) params.category_id = this.filterCategoryId;

    this.api.getTransactions(params).subscribe((data) => {
      this.transactions = data.items;
      this.total = data.total;
      this.cdr.detectChanges();
    });
  }

  applyFilter() {
    this.offset = 0;
    this.loadTransactions();
  }

  addTransaction() {
    if (!this.newTx.category_id || !this.newTx.amount) return;
    this.api.createTransaction(this.newTx).subscribe(() => {
      this.showForm = false;
      this.newTx = { amount: 0, description: '', type: 'expense', category_id: 0 };
      this.loadTransactions();
    });
  }

  deleteTransaction(id: number) {
    this.api.deleteTransaction(id).subscribe(() => {
      this.loadTransactions();
    });
  }

  nextPage() {
    if (this.offset + this.limit < this.total) {
      this.offset += this.limit;
      this.loadTransactions();
    }
  }

  prevPage() {
    if (this.offset > 0) {
      this.offset -= this.limit;
      this.loadTransactions();
    }
  }

  formatAmount(tx: Transaction): string {
    return tx.type === 'income' ? `+$${tx.amount.toFixed(2)}` : `-$${tx.amount.toFixed(2)}`;
  }

  formatDate(dateStr: string): string {
    return new Date(dateStr).toLocaleDateString('en-US', { month: '2-digit', day: '2-digit', year: 'numeric' });
  }

  getCategoryName(id: number): string {
    return this.categories.find((c) => c.id === id)?.name || '—';
  }
}
