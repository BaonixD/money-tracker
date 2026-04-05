import { Routes } from '@angular/router';
import { authGuard } from './core/auth-guard';
import { Login } from './auth/login/login';
import { Register } from './auth/register/register';
import { Dashboard } from './dashboard/dashboard';
import { CategoryList } from './categories/category-list/category-list';
import { TransactionList } from './transactions/transaction-list/transaction-list';

export const routes: Routes = [
  { path: 'login', component: Login },
  { path: 'register', component: Register },
  { path: 'dashboard', component: Dashboard, canActivate: [authGuard] },
  { path: 'categories', component: CategoryList, canActivate: [authGuard] },
  { path: 'transactions', component: TransactionList, canActivate: [authGuard] },
  { path: '', redirectTo: 'dashboard', pathMatch: 'full' },
  { path: '**', redirectTo: 'dashboard' },
];
