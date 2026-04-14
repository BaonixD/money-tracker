import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterLink } from '@angular/router';
import { ApiService } from '../core/api';
import { StatisticsResponse, Transaction } from '../shared/models/transaction.model';
import { Category } from '../shared/models/category.model';
import { forkJoin } from 'rxjs';

interface CategorySpending {
  name: string;
  amount: number;
  percent: number;
}

@Component({
  selector: 'app-dashboard',
  imports: [CommonModule, RouterLink],
  templateUrl: './dashboard.html',
  styleUrl: './dashboard.scss',
})
export class Dashboard implements OnInit {
  stats: StatisticsResponse = { total_income: 0, total_expense: 0, balance: 0 };
  recentTransactions: Transaction[] = [];
  categories: Category[] = [];
  categorySpending: CategorySpending[] = [];
  totalTransactions = 0;
  avgExpense = 0;
  biggestExpense: Transaction | null = null;

  constructor(private api: ApiService) {}

  ngOnInit() {
    forkJoin({
      stats: this.api.getStatistics(),
      transactions: this.api.getTransactions({ limit: 100, offset: 0 }),
      categories: this.api.getCategories(),
    }).subscribe(({ stats, transactions, categories }) => {
      this.stats = stats;
      this.categories = categories;
      this.totalTransactions = transactions.total;
      this.recentTransactions = transactions.items.slice(0, 5);

      const expenses = transactions.items.filter(t => t.type === 'expense');
      if (expenses.length > 0) {
        this.avgExpense = expenses.reduce((sum, t) => sum + t.amount, 0) / expenses.length;
        this.biggestExpense = expenses.reduce((max, t) => t.amount > max.amount ? t : max, expenses[0]);
      }

      // Category spending breakdown
      const spendingMap = new Map<number, number>();
      for (const tx of expenses) {
        spendingMap.set(tx.category_id, (spendingMap.get(tx.category_id) || 0) + tx.amount);
      }
      const totalExpense = expenses.reduce((sum, t) => sum + t.amount, 0);
      this.categorySpending = Array.from(spendingMap.entries())
        .map(([catId, amount]) => ({
          name: this.getCategoryName(catId),
          amount,
          percent: totalExpense > 0 ? (amount / totalExpense) * 100 : 0,
        }))
        .sort((a, b) => b.amount - a.amount);
    });
  }

  getCategoryName(id: number): string {
    return this.categories.find(c => c.id === id)?.name || '—';
  }

  formatAmount(tx: Transaction): string {
    if (tx.type === 'income') {
      return `+${tx.amount.toLocaleString()} ₸`;
    }
    return `-${tx.amount.toLocaleString()} ₸`;
  }

  formatMoney(amount: number): string {
    return `${amount.toLocaleString()} ₸`;
  }

  formatDate(dateStr: string): string {
    const date = new Date(dateStr);
    return date.toLocaleDateString('ru-RU', { day: '2-digit', month: '2-digit', year: 'numeric' });
  }
}
