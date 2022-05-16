<script setup>
import { ref, watch, computed } from "vue"
    const emit = defineEmits([
        "logout",
        "open-login",
        "open-registration"
    ])

    const props = defineProps({
        user: {
            type: Object,
            default: null
        }
    })

    const tabs = [
		{icon: 'fas fa-home', title: 'Home', path: "/", minAccessLevel: 0},
		{icon: 'far fa-user', title: 'Profile', path: `/profile/${props.user ? props.user.id : ''}`, minAccessLevel: 100},
        {icon: 'fas fa-hashtag', title: 'Explore', path: "/admin", minAccessLevel: 200},

	];

    const accessLevel = ref(0)
    watch(
        ()=>props.user,
        (newVal) => {
            if(newVal) {
                accessLevel.value = props.user.access_level
                tabs[1].path = `/profile/${props.user.id}`
            }
            else accessLevel.value = 0
        }
    )
    const tabsToShow = computed(() => {
        const accesibleRoutes = tabs.filter((tab) => {    
            return tab.minAccessLevel <= accessLevel.value
        })
        return accesibleRoutes
    })


	const dropdown = ref(false);
    const handleLogout = () => {
        dropdown.value = false
        emit("logout")
    }

    const openLogin = () => {
        emit("open-login")
    }

    const openRegistration = () => {
        emit("open-registration")
    }
    
</script>

<template>
    <aside class="flex flex-col justify-between px-2 py-2 border-r lg:w-1/5 border-lighter lg:px-6">
      <div>
        <router-link to="/" class="w-12 h-12 text-3xl rounded-full hover:bg-lightblue text-blue">
          <i class="fab fa-twitter"></i>
        </router-link>
        <router-link v-for="tab in tabsToShow" :to="tab.path || ''" :key="tab.to" class="flex items-center px-4 py-2 mb-3 mr-auto rounded-full focus:outline-none hover:text-blue hover:bg-lightblue">
            <i :class="`${ tab.icon } text-2xl mr-4 text-left`"></i>
            <span class="hidden text-lg font-semibold text-left lg:block"> {{ tab.title }} </span>
        </router-link>
        <!--
        <button class="w-12 h-12 p-3 font-semibold text-white rounded-full bg-blue focus:outline-none lg:h-auto lg:w-full hover:bg-darkblue">
          <p class="hidden lg:block">Tweet</p>
          <i class="fas fa-plus lg:hidden"></i>
        </button>
        -->
      </div>

    <div v-if="props.user" class="relative lg:w-full">
        <button @click="dropdown = true" class="flex items-center w-full p-2 rounded-full hover:bg-lightblue focus:outline-none">
          <img :src="props.user.user_image" class="w-10 h-10 border rounded-full border-lighter" />
          <div class="hidden ml-4 lg:block">
            <p class="text-sm font-bold leading-tight"> {{ props.user.user_email }} </p>
            <p class="text-sm leading-tight"> @{{ props.user.user_name }} </p>
          </div>
          <i class="hidden ml-auto text-lg lg:block fas fa-angle-down"></i>
        </button>
    </div>
    <div v-else class="relative lg:w-full">
        <button @click="openLogin" class="flex items-center w-full p-2 rounded-full hover:bg-lightblue focus:outline-none">
          <div class="ml-4">
            <p class="text-sm font-bold leading-tight"> Login </p>
          </div>
        </button>
        <button @click="openRegistration" class="flex items-center w-full p-2 rounded-full hover:bg-lightblue focus:outline-none">
          <div class="ml-4">
            <p class="text-sm font-bold leading-tight"> Sign up </p>
          </div>
        </button>
    </div>

        <!--Dropdown-->
        <div v-if="dropdown === true" class="absolute bottom-0 left-0 w-64 mb-16 bg-white rounded-lg shadow-md border-lightest">
          <button @click="dropdown = false" class="flex items-center w-full p-3 hover:bg-lightest focus:outline-none">
            <img :src="user.user_image" class="w-10 h-10 border rounded-full border-lighter" />
            <div class="ml-4">
              <p class="text-sm font-bold leading-tight"> {{ user.user_first_name }} {{ user.user_last_name }}</p>
              <p class="text-sm leading-tight"> @{{ user.user_name }} </p>
            </div>
            <i class="ml-auto fas fa-check test-blue"></i>
          </button>
          <button @click="handleLogout" class="w-full p-3 text-left border-t hover:bg-lightest border-lighter test-sm focus:outline-none">
            Log out {{ user.user_name }}
          </button>
        </div>

    </aside>
    
</template>