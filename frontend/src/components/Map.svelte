<script>

    import {onMount} from "svelte";
    import {mapMode, mapFloorLevel, mapOpenSearchMenu} from '../store.js';
    import { fade } from 'svelte/transition';
    import MapLayer from "./MapLayer.svelte";
    import MapSearch from "./MapSearch.svelte";
    import SearchIcon from "./icons/SearchIcon.svelte";
    import ArrowUpIcon from "./icons/ArrowUpIcon.svelte";
    import ArrowDownIcon from "./icons/ArrowDownIcon.svelte";
    import LayersIcon from "./icons/LayersIcon.svelte";

    export let mapURL

    let data = [];
    let layers = [];

    onMount(async () => {
        const res = await fetch(mapURL);
        data = await res.json();
        layers = data.layers;
    });

    async function changeMapMode() {
        if ($mapMode === 'view_building' & $mapFloorLevel !== null) {
            await mapMode.updateMode('view_floor')
        } else {
            await mapMode.updateMode('view_building')
            await mapFloorLevel.updateLevel(null);
        }
    }

    async function changeConditionSearchMenu() {
        $mapOpenSearchMenu ? await mapOpenSearchMenu.isClose() : await mapOpenSearchMenu.isOpen()
    }

    async function checkIncrementOrDecrementLayerAdd(direction) {
        if (direction === 'up') {
            if ($mapFloorLevel + 1 <= layers.length) {
                return true
            }
        } else if (direction === 'down') {
            if ($mapFloorLevel - 1 > 0 ) {
                return true
            }
        }
        return false
    }

    async function changeActiveLayerDown() {
        if (await checkIncrementOrDecrementLayerAdd('down')) {
            await mapFloorLevel.decrement()
        }
    }

    async function changeActiveLayerUp() {
        if (await checkIncrementOrDecrementLayerAdd('up')) {
            await mapFloorLevel.increment()
        }
    }

</script>

<div class="main">
    <header class="map-header">
        <h1>{data.title} / {$mapFloorLevel ? 'Этаж ' + $mapFloorLevel : 'Этаж не выбран'}</h1>
    </header>
    <div class="space">
        <div class="background" class:background-hidden="{$mapMode === 'view_floor'}">
            <img class="background-map" src="{data.background}" alt="background"/>
        </div>
        <div class="levels">
            {#each layers as layer}
                <MapLayer level="{layer.id}" layer="{layer}" />
            {:else}
                <p>Загрузка</p>
            {/each}
            <slot/>
        </div>
    </div>
    <button on:click={changeConditionSearchMenu} class="boxbutton boxbutton-dark open-search" aria-label="Show search">
        <svg class="icon icon-search">
            <SearchIcon/>
        </svg>
    </button>
    {#if $mapMode === 'view_floor'}
        <nav class="space-nav" transition:fade="{{ duration: 400 }}">
            <button on:click={changeActiveLayerUp} class="boxbutton space-nav-button-up search-mode-buttons-icon" >
                <ArrowUpIcon/>
            </button>
            <button on:click={changeMapMode} class="boxbutton boxbutton-dark space-nav_button-all-levels search-mode-buttons-icon">
                <LayersIcon/>
            </button>
            <button on:click={changeActiveLayerDown} class="boxbutton space-nav-button-down search-mode-buttons-icon">
                <ArrowDownIcon/>
            </button>
        </nav>
    {/if}
</div>
<aside class="{$mapOpenSearchMenu ? 'spaces-list spaces-list-open' : 'spaces-list'}" id="spaces-list">
    <MapSearch layers="{layers}"/>
    <div class="search">
        <input class="search-input" placeholder="Search..." />
        <button on:click={changeConditionSearchMenu} class="boxbutton boxbutton-darker close-search">
            <svg class="icon icon-cross">
                <SearchIcon/>
            </svg>
        </button>
    </div>
</aside>



<style>

    /* Header */

    .map-header {
        position: absolute;
        z-index: 100;
        top: 0;
        left: 0;
        display: -webkit-flex;
        display: flex;
        -webkit-align-items: center;
        align-items: center;
        padding: 1.5em 1em;
        text-align: center;
    }

    .map-header h1 {
        font-size: 1.15em;
        font-weight: normal;
        line-height: 1;
        margin: 0 0 0 1em;
    }

    /* Levels main */

    .background,
    .levels {
        position: absolute;
        top: 50%;
        left: 50%;
    }

    .background {
        width: 192vmin;
        /* double of space map */
        height: 128vmin;
        margin: -64vmin 0 0 -96vmin;
        pointer-events: none;
        -webkit-transition: opacity 0.8s;
        transition: opacity 0.8s;
        -webkit-transform-style: preserve-3d;
        transform-style: preserve-3d;
    }

    .background-map {
        opacity: 0.3;
        max-width: 100%;
        display: block;
    }

    .background-hidden {
        opacity: 0;
    }

    .levels {
        width: 96vmin;
        height: 64vmin;
        margin: -32vmin 0 0 -48vmin;
        -webkit-transition: -webkit-transform 0.3s;
        transition: transform 0.3s;
        -webkit-transform-style: preserve-3d;
        transform-style: preserve-3d;
    }

    .background,
    .levels {
        -webkit-transform: rotateX(70deg) rotateZ(-45deg) translateZ(-15vmin);
        transform: rotateX(70deg) rotateZ(-45deg) translateZ(-15vmin);
    }

    /* Level nav */
    .main {
        position: fixed;
        top: 0;
        left: 0;
        overflow: hidden;
        width: calc(100vw - 300px);
        height: 100vh;
    }

    .space {
        position: relative;
        width: 100%;
        height: 100%;
        pointer-events: none;
        -webkit-perspective: 3500px;
        perspective: 3500px;
        -webkit-perspective-origin: 0% 50%;
        perspective-origin: 0% 50%;
        -webkit-transition: -webkit-transform 0.8s;
        transition: transform 0.8s;
        -webkit-transition-timing-function: cubic-bezier(0.2, 1, 0.3, 1);
        transition-timing-function: cubic-bezier(0.2, 1, 0.3, 1);
    }


    .space-nav {
        position: absolute;
        top: 0;
        right: 0;
        text-align: center;
        -webkit-transition: opacity 0.8s;
        transition: opacity 0.8s;
    }

    /* Spaces list (sidebar) */

    .spaces-list {
        position: absolute;
        top: 0;
        right: 0;
        width: 300px;
        min-height: 100vh;
        padding: 5em 0 1em;
        background: #fff;
    }

    /* Search list (sidebar) */

    .search {
        position: fixed;
        z-index: 100;
        top: 0;
        right: 0;
        left: calc(100vw - 300px);
    }

    .search-input {
        width: 100%;
        padding: 1.315em 2em;
        color: #fff;
        border: 0;
        background: #515158;
        border-radius: 0;
    }

    .search-input:focus {
        outline: none;
    }

    :global(.search-mode-buttons-icon svg) {
        height: 32px;
        width: 32px;
        fill: white;
    }

    :global(.search-mode-buttons-icon) {
        cursor: pointer;
    }
</style>