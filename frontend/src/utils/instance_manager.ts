/**
 * Instance Manager
 *
 * Prevents multiple instances of the Vue.js application from running simultaneously.
 */

class InstanceManager {
  private static readonly STORAGE_KEY = 'financing_instance_id'
  private static readonly HEARTBEAT_INTERVAL = 30000 // 30 seconds

  private instanceId: string
  private heartbeatTimer: number | null = null

  constructor() {
    this.instanceId = this.generateInstanceId()
  }

  private generateInstanceId(): string {
    return `financing_${Date.now()}_${Math.random().toString(36).substring(2, 9)}`
  }

  async checkExistingInstance(): Promise<boolean> {
    try {
      const existingId = localStorage.getItem(InstanceManager.STORAGE_KEY)
      if (existingId) {
        console.log('Existing instance found:', existingId)
        return true
      }
      return false
    } catch (error) {
      console.error('Error checking existing instance:', error)
      return false
    }
  }

  async registerInstance(): Promise<void> {
    try {
      localStorage.setItem(InstanceManager.STORAGE_KEY, this.instanceId)
      console.log('Registered instance:', this.instanceId)
      await this.startHeartbeat()
    } catch (error) {
      console.error('Error registering instance:', error)
    }
  }

  async unregisterInstance(): Promise<void> {
    try {
      this.stopHeartbeat()
      localStorage.removeItem(InstanceManager.STORAGE_KEY)
      console.log('Unregistered instance')
    } catch (error) {
      console.error('Error unregistering instance:', error)
    }
  }

  private async startHeartbeat(): Promise<void> {
    this.stopHeartbeat()

    this.heartbeatTimer = window.setInterval(async () => {
      try {
        const response = await fetch('/api/health', {
          method: 'GET',
          cache: 'no-cache'
        })
        if (!response.ok) {
          console.warn('Health check failed, stopping heartbeat')
          this.stopHeartbeat()
        }
      } catch (error) {
        console.error('Heartbeat error:', error)
        this.stopHeartbeat()
      }
    }, InstanceManager.HEARTBEAT_INTERVAL)

    console.log('Heartbeat started')
  }

  private stopHeartbeat(): void {
    if (this.heartbeatTimer !== null) {
      clearInterval(this.heartbeatTimer)
      this.heartbeatTimer = null
      console.log('Heartbeat stopped')
    }
  }

  async preventMultipleInstances(): Promise<boolean> {
    const hasExisting = await this.checkExistingInstance()

    if (hasExisting) {
      const confirm = window.confirm(
        'Another instance of Financing is already running.\n\n' +
        'Do you want to close the existing instance and continue?'
      )

      if (confirm) {
        await this.unregisterInstance()
        console.log('Existing instance unregistered')
        return true
      } else {
        console.log('User chose not to replace existing instance')
        return false
      }
    }

    await this.registerInstance()
    return true
  }

  async cleanup(): Promise<void> {
    await this.unregisterInstance()
    console.log('Instance cleanup completed')
  }
}

export default InstanceManager
