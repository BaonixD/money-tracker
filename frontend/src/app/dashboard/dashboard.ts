import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ApiService } from '../core/api';
import { StatisticsResponse, Transaction } from '../shared/models/transaction.model';

@Component({
  selector: 'app-dashboard',
  imports: [CommonModule],
  templateUrl: './dashboard.html',
  styleUrl: './dashboard.scss',
})
export class Dashboard implements OnInit {
  stats: StatisticsResponse = { total_income: 0, total_expense: 0, balance: 0 };
  recentTransactions: Transaction[] = [];

  constructor(private api: ApiService) {}

  ngOnInit() {
    this.api.getStatistics().subscribe((data) => {
      this.stats = data;
    });

    this.api.getTransactions({ limit: 5, offset: 0 }).subscribe((data) => {
      this.recentTransactions = data.items;
    });
  }

  formatAmount(tx: Transaction): string {
    if (tx.type === 'income') {
      return `+$${tx.amount.toFixed(2)}`;
    }
    return `-$${tx.amount.toFixed(2)}`;
  }

  formatDate(dateStr: string): string {
    const date = new Date(dateStr);
    return date.toLocaleDateString('en-US', { month: '2-digit', day: '2-digit', year: 'numeric' });
  }
}
