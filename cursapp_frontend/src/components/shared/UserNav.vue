<template>
  <div class="flex items-center gap-4">
    
    <DropdownMenu>
      <DropdownMenuTrigger as-child>
        <Button variant="ghost" class="relative h-10 w-10 rounded-full">
          <Avatar class="h-10 w-10">
            <AvatarImage 
              v-if="authStore.user?.foto_perfil" 
              :src="authStore.user.foto_perfil" 
              :alt="authStore.user.username" 
            />
            <AvatarFallback>
              {{ authStore.user?.username?.substring(0, 2).toUpperCase() || 'U' }}
            </AvatarFallback>
          </Avatar>
        </Button>
      </DropdownMenuTrigger>
      <DropdownMenuContent class="w-56" align="end">
        <DropdownMenuLabel class="flex flex-col space-y-1">
          <p class="text-sm font-medium leading-none">{{ authStore.user?.username }}</p>
          <p class="text-xs leading-none text-muted-foreground">
            {{ authStore.user?.email }}
          </p>
        </DropdownMenuLabel>
        
        <DropdownMenuSeparator />
        <DropdownMenuItem class="focus:bg-transparent cursor-default sm:hidden">
            <Trophy class="mr-2 h-4 w-4 text-amber-400" />
            <span>{{ authStore.user?.xp_totales || 0 }} XP</span>
        </DropdownMenuItem>
        <DropdownMenuSeparator class="sm:hidden" />

        <DropdownMenuGroup>
          <DropdownMenuItem>
            <User class="mr-2 h-4 w-4" />
            <span>Perfil</span>
          </DropdownMenuItem>
        </DropdownMenuGroup>
        <DropdownMenuSeparator />
        <DropdownMenuItem @click="onLogout" class="text-destructive focus:text-destructive">
          <LogOut class="mr-2 h-4 w-4" />
          <span>Cerrar Sesión</span>
        </DropdownMenuItem>
      </DropdownMenuContent>
    </DropdownMenu>

    <div class="hidden sm:flex items-center gap-2">
      <Trophy class="h-5 w-5 text-amber-400" />
      <span class="text-sm font-medium text-foreground">
        {{ authStore.user?.xp_totales || 0 }} XP
      </span>
    </div>
    
  </div>
  </template>

<script setup lang="ts">
import { useAuthStore } from '@/store/auth.store';
import { Avatar, AvatarFallback, AvatarImage } from '@/components/ui/avatar';
import { Button }  from '@/components/ui/button';
import {
    DropdownMenu,
    DropdownMenuContent,
    DropdownMenuGroup,
    DropdownMenuItem,
    DropdownMenuLabel,
    DropdownMenuSeparator,
    DropdownMenuTrigger,
} from '@/components/ui/dropdown-menu';
import { LogOut, User, Trophy } from 'lucide-vue-next';

const authStore = useAuthStore();
const onLogout = () => {
    authStore.logout();
}
</script>