import { Component } from '@angular/core';
import { RouterOutlet, Router } from '@angular/router';
import { CommonModule } from '@angular/common';
import { Sidebar } from './shared/sidebar/sidebar';

@Component({
  selector: 'app-root',
  imports: [RouterOutlet, CommonModule, Sidebar],
  templateUrl: './app.html',
  styleUrl: './app.scss',
})
export class App {
  constructor(public router: Router) {}

  showSidebar(): boolean {
    const url = this.router.url;
    return url !== '/login' && url !== '/register';
  }
}
