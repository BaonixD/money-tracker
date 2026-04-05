import { Component } from '@angular/core';
import { RouterLink, RouterLinkActive } from '@angular/router';
import { AuthService } from '../../core/auth';

@Component({
  selector: 'app-sidebar',
  imports: [RouterLink, RouterLinkActive],
  templateUrl: './sidebar.html',
  styleUrl: './sidebar.scss',
})
export class Sidebar {
  collapsed = false;

  constructor(private authService: AuthService) {}

  toggle() {
    this.collapsed = !this.collapsed;
  }

  logout() {
    this.authService.logout();
  }
}
