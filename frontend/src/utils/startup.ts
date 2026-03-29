/**
 * Startup Script
 *
 * Manages single instance and port availability on application startup.
 */

import InstanceManager from './instance_manager'

async function initializeApplication(): Promise<void> {
  console.log('Initializing Financing application...')

  try {
    // Check for existing instances
    const instanceManager = new InstanceManager()
    const canStart = await instanceManager.preventMultipleInstances()

    if (!canStart) {
      console.log('Application startup cancelled by user')
      window.location.href = 'about:blank'
      return
    }

    console.log('Application starting successfully')

    // Register cleanup on page unload
    window.addEventListener('beforeunload', async () => {
      await instanceManager.cleanup()
      console.log('Cleanup on page unload')
    })

    // Register visibility change handler
    document.addEventListener('visibilitychange', async () => {
      if (document.hidden) {
        console.log('Application hidden')
      } else {
        console.log('Application visible')
      }
    })

  } catch (error) {
    console.error('Failed to initialize application:', error)
    alert('Failed to initialize application. Please refresh the page.')
  }
}

// Auto-initialize when script loads
initializeApplication()
